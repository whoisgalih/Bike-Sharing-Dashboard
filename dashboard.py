import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Load data
hour_data = pd.read_csv("hour_df.csv")
day_data = pd.read_csv("day_df.csv")

# Sidebar
st.sidebar.title("Bicycle Sharing Dashboard")
page = st.sidebar.radio("Choose a page", ["Home", "Weather", "Seasonal"])

# Home and weather sidebar
if page == "Weather" or page == "Home":
    # Min and max date
    min_date = pd.to_datetime(hour_data["dteday"]).min().date()
    max_date = pd.to_datetime(hour_data["dteday"]).max().date()

    # Select date range
    try:
        start_date, end_date = st.sidebar.date_input(
            "Select date range",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
        )
    except ValueError:
        st.error("Please select a valid date range.")
        st.stop()

# Home page
if page == "Home":
    st.title("Bicycle Sharing Dashboard")
    st.write("This dashboard shows the bike sharing data.")

    st.subheader(f"Trend of Bike Sharing Over Time From {start_date} to {end_date}")

    # Filter date
    filtered_data = day_data[
        (day_data["dteday"] >= str(start_date)) & (day_data["dteday"] <= str(end_date))
    ]

    # Plot
    st.line_chart(filtered_data[["cnt", "dteday"]].set_index("dteday"))

# Weather page
if page == "Weather":
    st.title("Bike Sharing Based on Weather")
    st.write("This page shows the bike sharing based on weather conditions.")

    # Multiselect for weather conditions
    weather_conditions = st.multiselect(
        "Choose weather conditions", hour_data["weathersit"].unique()
    )

    # Check if conditions are selected
    if len(weather_conditions) == 0:
        st.stop()

    # Filter date
    filtered_data = hour_data[
        (hour_data["dteday"] >= str(start_date))
        & (hour_data["dteday"] <= str(end_date))
    ]

    # Filter weather conditions
    filtered_data = hour_data[hour_data["weathersit"].isin(weather_conditions)]

    # Group by weather condition
    grouped_data = (
        filtered_data.groupby("weathersit")["cnt"]
        .sum()
        .reset_index()
        .sort_values(by="cnt", ascending=False)
    )

    # Plot title
    st.subheader(
        f"Bike Sharing Based on Weather Conditions From {start_date} to {end_date}"
    )

    # Plot
    fig, ax = plt.subplots()
    sns.barplot(data=grouped_data, x="weathersit", y="cnt", ax=ax)
    ax.set_title("Bike Sharing Based on Weather Conditions")
    ax.set_xlabel("Weather Condition")
    ax.set_ylabel("Total Bike Sharing")
    st.pyplot(fig)


# Seasonal sidebar
if page == "Seasonal":
    # Pic a year
    year = st.sidebar.selectbox("Choose a year", day_data["yr"].unique())

# Seasonal page
if page == "Seasonal":
    st.title("Bike Sharing Based on Seasonal Conditions")
    st.write("This page shows the bike sharing based on seasonal conditions.")

    # Single select for seasons
    season = st.selectbox("Choose a season", day_data["season"].unique())

    # Filter data
    filtered_data = day_data[(day_data["yr"] == year) & (day_data["season"] == season)]

    # Plot title
    # Centered title
    st.markdown(f"<h3>{season} {year}</h3>", unsafe_allow_html=True)

    # Plot
    st.line_chart(filtered_data[["cnt", "dteday"]].set_index("dteday"))
