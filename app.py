
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
st.title("IMDB Top 1000 Movies Explorer")

# Sidebar Navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home", "Explore Data", "Visualizations"])

# Load dataset
file_path = "imdb_top_1000.csv"
data = load_data(file_path)

if data is not None:
    # Home Page
    if menu == "Home":
        st.header("Welcome to the IMDB Top 1000 Movies Explorer!")
        st.write("""
            This app allows you to explore the top 1000 IMDB movies dataset. 
            Use the sidebar to navigate through the app.
            
            Features include:
            - Viewing and filtering the dataset.
            - Visualizing movies by year, genre, director, and ratings.
            - Dynamic graphs based on selected filters.
            
            Start by exploring the dataset or visualizing key insights!
        """)

    # Explore Data Page
    elif menu == "Explore Data":
        st.header("Explore the Dataset")

        # Display full dataset
        if st.checkbox("Show Full Dataset"):
            st.dataframe(data)

        # Filter by Genre
        genres = data['Genre'].dropna().str.split(',').explode().unique()
        selected_genre = st.multiselect("Filter by Genre", options=sorted(genres), default=[])
        filtered_data = data[data['Genre'].apply(lambda x: any(genre in x for genre in selected_genre) if pd.notnull(x) else False)] if selected_genre else data

        # Filter by Year
        years = sorted(data['Released_Year'].dropna().unique())
        selected_year = st.multiselect("Filter by Year", options=years, default=[])
        filtered_data = filtered_data[filtered_data['Released_Year'].isin(selected_year)] if selected_year else filtered_data

        # Display filtered dataset
        st.write(f"Filtered Dataset: {len(filtered_data)} records")
        st.dataframe(filtered_data)

    # Visualizations Page
    elif menu == "Visualizations":
        st.header("Visualizations")

        # Filter by Genre and Year for Visualizations
        genres = data['Genre'].dropna().str.split(',').explode().unique()
        selected_genre = st.multiselect("Filter by Genre", options=sorted(genres), default=[])
        filtered_data = data[data['Genre'].apply(lambda x: any(genre in x for genre in selected_genre) if pd.notnull(x) else False)] if selected_genre else data

        years = sorted(data['Released_Year'].dropna().unique())
        selected_year = st.multiselect("Filter by Year", options=years, default=[])
        filtered_data = filtered_data[filtered_data['Released_Year'].isin(selected_year)] if selected_year else filtered_data

        # Movies by Year
        if st.checkbox("Show Movies by Year"):
            if "Released_Year" in filtered_data.columns:
                movies_per_year = filtered_data['Released_Year'].value_counts().sort_index()
                plt.figure(figsize=(10, 6))
                plt.bar(movies_per_year.index.astype(str), movies_per_year.values, color="skyblue")
                plt.title("Movies by Year")
                plt.xlabel("Year")
                plt.ylabel("Number of Movies")
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.warning("The dataset does not contain a 'Released_Year' column.")

        # Top Directors
        if st.checkbox("Show Top Directors"):
            if "Director" in filtered_data.columns:
                top_directors = filtered_data['Director'].value_counts().head(10)
                st.bar_chart(top_directors)
            else:
                st.warning("The dataset does not contain a 'Director' column.")

        # Ratings Distribution
        if st.checkbox("Show Ratings Distribution"):
            if "IMDB_Rating" in filtered_data.columns:
                plt.figure(figsize=(10, 6))
                plt.hist(filtered_data['IMDB_Rating'].dropna(), bins=10, edgecolor='k', alpha=0.7, color="orange")
                plt.title("IMDB Ratings Distribution")
                plt.xlabel("Rating")
                plt.ylabel("Frequency")
                st.pyplot(plt)
            else:
                st.warning("The dataset does not contain an 'IMDB_Rating' column.")

        # Average Ratings by Year
        if st.checkbox("Show Average Ratings by Year"):
            if "Released_Year" in filtered_data.columns and "IMDB_Rating" in filtered_data.columns:
                avg_ratings_per_year = filtered_data.groupby("Released_Year")["IMDB_Rating"].mean()
                plt.figure(figsize=(10, 6))
                plt.plot(avg_ratings_per_year.index, avg_ratings_per_year.values, marker="o", color="green")
                plt.title("Average IMDB Ratings by Year")
                plt.xlabel("Year")
                plt.ylabel("Average Rating")
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.warning("The dataset does not contain the required columns 'Released_Year' and 'IMDB_Rating'.")
else:
    st.error("Dataset could not be loaded. Please ensure the file is in the correct directory.")
