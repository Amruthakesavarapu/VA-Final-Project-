import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# App title
st.title("🎥 IMDB Top 1000 Movies")

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Visualizations", "Data Source"])

# Load dataset
file_path = "imdb_top_1000.csv"
data = load_data(file_path)

if data is not None:
    # Home Page
    if menu == "Home":
        st.header("Welcome to the IMDB Top 1000 Movies!")
        st.image("https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg", use_column_width=True)

        st.subheader("Purpose of the Project")
        st.write("""
            The purpose of this project is to analyze the IMDB Top 1000 movies dataset to uncover trends and insights 
            about the movie industry. This app provides tools to:
            - Explore ratings trends over the years.
            - Identify the most successful directors and genres.
            - Understand audience preferences through data visualizations.
        """)

        

    # Visualizations Page
    elif menu == "Visualizations":
        st.header("Visualizations")

        # Dropdown filters for Genre and Year
        st.subheader("Filters")
        genres = data['Genre'].dropna().str.split(',').explode().unique()
        selected_genre = st.selectbox("Select Genre", options=["All"] + sorted(genres), index=0)

        years = sorted(data['Released_Year'].dropna().unique())
        selected_year = st.selectbox("Select Year", options=["All"] + years, index=0)

        # Apply filters
        filtered_data = data.copy()
        if selected_genre != "All":
            filtered_data = filtered_data[filtered_data['Genre'].apply(
                lambda x: selected_genre in x if pd.notnull(x) else False
            )]
        if selected_year != "All":
            filtered_data = filtered_data[filtered_data['Released_Year'] == selected_year]

        st.write(f"Filtered Dataset: {len(filtered_data)} records")

        # Visualization 1: Movies by Year
        if "Released_Year" in filtered_data.columns:
            movies_per_year = filtered_data['Released_Year'].value_counts().sort_index()
            if not movies_per_year.empty:
                st.write("### Movies by Year")
                plt.figure(figsize=(10, 6))
                plt.bar(movies_per_year.index.astype(str), movies_per_year.values, color="skyblue")
                plt.title("Movies by Year")
                plt.xlabel("Year")
                plt.ylabel("Number of Movies")
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.warning("No data available for this filter.")

        # Visualization 2: Top Directors
        if "Director" in filtered_data.columns:
            top_directors = filtered_data['Director'].value_counts().head(10)
            if not top_directors.empty:
                st.write("### Top Directors")
                st.bar_chart(top_directors)
            else:
                st.warning("No data available for this filter.")

        # Visualization 3: Ratings Distribution
        if "IMDB_Rating" in filtered_data.columns:
            if not filtered_data["IMDB_Rating"].dropna().empty:
                st.write("### IMDB Ratings Distribution")
                plt.figure(figsize=(10, 6))
                plt.hist(filtered_data['IMDB_Rating'].dropna(), bins=10, edgecolor='k', alpha=0.7, color="orange")
                plt.title("IMDB Ratings Distribution")
                plt.xlabel("Rating")
                plt.ylabel("Frequency")
                st.pyplot(plt)
            else:
                st.warning("No data available for this filter.")

        # Visualization 4: Average Ratings by Year
        if "Released_Year" in filtered_data.columns and "IMDB_Rating" in filtered_data.columns:
            avg_ratings_per_year = filtered_data.groupby("Released_Year")["IMDB_Rating"].mean()
            if not avg_ratings_per_year.empty:
                st.write("### Average IMDB Ratings by Year")
                plt.figure(figsize=(10, 6))
                plt.plot(avg_ratings_per_year.index, avg_ratings_per_year.values, marker="o", color="green")
                plt.title("Average IMDB Ratings by Year")
                plt.xlabel("Year")
                plt.ylabel("Average Rating")
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.warning("No data available for this filter.")

    # Data Source Page
    elif menu == "Data Source":
        st.header("Data Source")
        st.write("""
            The dataset used in this application is the IMDB Top 1000 Movies dataset. 
            
            Source Information:
            - The data was collected from the "https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows".
            - Columns include:
              - Movie details such as Title, Genre, Director, and Ratings.
              - Release Year and Audience Ratings.
            
        """)
else:
    st.error("Dataset could not be loaded. Please ensure the file is in the correct directory.")
