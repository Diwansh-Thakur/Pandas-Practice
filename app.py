import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load and cache data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")

    # Clean and fix 'date_added' column
    df['date_added'] = pd.to_datetime(df['date_added'].astype(str).str.strip(), format="%B %d, %Y", errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month_name()

    # Fill NA values for consistency
    df['country'] = df['country'].fillna("Unknown")
    df['rating'] = df['rating'].fillna("Not Rated")
    df['duration'] = df['duration'].fillna("Unknown")
    
    return df

# Load the dataset
df = load_data()

# App Title
st.title("🎬 Netflix Data Analysis Dashboard")

# Dataset Overview
st.subheader("Dataset Overview")
st.write(df.head())

# Filters
st.sidebar.header("Filter Content")
selected_type = st.sidebar.multiselect("Select Type", df['type'].unique(), default=df['type'].unique())
selected_country = st.sidebar.multiselect("Select Country", df['country'].unique(), default=["United States", "India", "United Kingdom"])
filtered_df = df[(df['type'].isin(selected_type)) & (df['country'].isin(selected_country))]

# Show filtered data
st.subheader("Filtered Data Preview")
st.write(filtered_df.head())

# Content by Type
st.subheader("Total Content by Type")
type_counts = df['type'].value_counts()
fig1, ax1 = plt.subplots()
sns.barplot(x=type_counts.index, y=type_counts.values, ax=ax1)
ax1.set_ylabel("Number of Titles")
ax1.set_xlabel("Type")
st.pyplot(fig1)

# Content Over Time
st.subheader("Content Added Over the Years")
yearly_content = df['year_added'].value_counts().sort_index()
fig2, ax2 = plt.subplots()
yearly_content.plot(kind='line', marker='o', ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Titles Added")
st.pyplot(fig2)

# Top Countries
st.subheader("Top Countries Producing Content")
top_countries = df['country'].value_counts().head(10)
fig3, ax3 = plt.subplots()
sns.barplot(y=top_countries.index, x=top_countries.values, ax=ax3)
ax3.set_xlabel("Number of Titles")
ax3.set_ylabel("Country")
st.pyplot(fig3)

# Genre/Category Analysis
st.subheader("Most Frequent Genres")
df['listed_in'] = df['listed_in'].fillna("Unknown")
all_genres = df['listed_in'].str.split(', ')
genre_counts = pd.Series([genre for sublist in all_genres.dropna() for genre in sublist]).value_counts().head(10)
fig4, ax4 = plt.subplots()
sns.barplot(y=genre_counts.index, x=genre_counts.values, ax=ax4)
ax4.set_xlabel("Number of Titles")
ax4.set_ylabel("Genre")
st.pyplot(fig4)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit by **Diwansh**")

