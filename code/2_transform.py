import pandas as pd
import streamlit as st
import pandaslib as pl

# Load data from cache, create combined col dataframe
states_data = pd.read_csv("cache/states.csv")
survey_data = pd.read_csv("cache/survey.csv")

unique_years = survey_data["year"].unique()
year_data_list = []
for year in unique_years:
    year_df = pd.read_csv(f"cache/col_{year}.csv")
    year_data_list.append(year_df)

col_data = pd.concat(year_data_list, ignore_index = True)

# Merging survey and COL data
survey_data["_country"] = survey_data["What country do you work in?"].apply(pl.clean_country_usa)
survey_states_combined = pd.merge(survey_data, states_data, how = "inner",
                                  left_on = "If you're in the U.S., what state do you work in?",
                                  right_on = "State")

survey_states_combined["_full_city"] = survey_states_combined["What city do you work in?"] + ", " + survey_states_combined["Abbreviation"] + ", " + survey_states_combined["_country"]
combined = pd.merge(survey_states_combined, col_data, how = "inner",
                    left_on = ["year", "_full_city"], right_on = ["year", "City"])

# Normalization
combined["_annual_salary_cleaned"] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)
combined["_annual_salary_adjusted"] = combined.apply(lambda row: row["_annual_salary_cleaned"] * (100 / row["Cost of Living Index"]), axis=1)

# Producing reports
combined.to_csv("cache/survey_dataset.csv")

adj_by_la = combined.pivot_table(index = "_full_city", columns = "How old are you?", values = "_annual_salary_adjusted", aggfunc = "mean")
adj_by_la.to_csv("cache/annual_salary_adjusted_by_location_and_age.csv")

adj_by_le = combined.pivot_table(index = "_full_city", columns = "What is your highest level of education completed?", values = "_annual_salary_adjusted", aggfunc = "mean")
adj_by_le.to_csv("cache/annual_salary_adjusted_by_location_and_education.csv")




