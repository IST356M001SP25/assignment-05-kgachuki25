import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
  
# Extract and save states.csv
states = pd.read_csv("https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv")
states.to_csv("cache/states.csv")

# Extract survey data
survey_data = pd.read_csv("https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv")
survey_data["year"] = survey_data["Timestamp"].apply(pl.extract_year_mdy)
survey_data.to_csv("cache/survey.csv")

# Unique years, creating csv for each
unique_years = survey_data["year"].unique()
for year in unique_years:
    year_data = pd.read_html(f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0")
    year_df = year_data[1] # Get correct df from list
    year_df["year"] = year # New column to label year
    year_df.to_csv(f"cache/col_{year}.csv")
