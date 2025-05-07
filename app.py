import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

# Load data
df = pd.read_csv('Social Media Users.csv')
platforms = sorted(df['Platform'].dropna().unique())  # Correct platform list
country_list = df['Country'].sort_values(ascending=True).unique().tolist()
df['Date Joined'] = pd.to_datetime(df['Date Joined'])
st.set_page_config(page_title='Social Media User Analysis', layout="wide")


# Platform analysis function
def platform_analysis(selected_platform):
    st.subheader(f'Average Time Spent on {selected_platform} by Country')

    # Compute average daily time by country for selected platform
    country_mean = (
        df[df['Platform'] == selected_platform]
        .groupby('Country')['Daily Time Spent (min)']
        .mean()
        .sort_values(ascending=False)
    )

    # Let user choose how many countries to display
    top_n = st.slider('Select number of top countries to display', 3, min(20, len(country_mean)), 5)
    top_data = country_mean.head(top_n)

    # Bar chart (cleaner than pie chart)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top_data.index[::-1], top_data[::-1], color='skyblue')
    ax.set_xlabel('Average Daily Time (min)')
    ax.set_title(f'Top {top_n} Countries using {selected_platform}')
    plt.tight_layout()
    st.pyplot(fig)

    # Optional full data table
    with st.expander('Show Full Country Data Table'):
        st.dataframe(country_mean.reset_index().rename(columns={'Daily Time Spent (min)': 'Avg Time (min)'}))
        # create 2 col to show highest time spend country and lowest

    col1, col2 = st.columns(2)
    country_mean.max()

    with col1:
        st.metric('Highest Time Spend Country', str(country_mean.max()) + ' min')
        st.metric('Country Name', str(country_mean.index[0]))

    with col2:
        st.metric('Lowest Time Spend Country', str(country_mean.min()) + ' min')
        st.metric('Country Name', str(country_mean.index[-1]))

    country_counts = df['Country'].value_counts().nlargest(50)  # Top 10 countries
    fig = px.pie(values=country_counts.values, names=country_counts.index,
                 title="User Distribution by Country")
    st.plotly_chart(fig)

    # Count the number of verified and unverified accounts across the whole dataset
    # Loop over platforms to plot pie charts for each platform's verified status

    platform_data = df[df['Platform'] == selected_platform]
    verified_counts = platform_data['Verified Account'].value_counts()

    # Plot a pie chart for each platform
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.pie(verified_counts, labels=verified_counts.index, autopct='%1.1f%%', colors=['#66b3ff', '#99ff99'])
    ax.set_title(f'Verified vs Unverified Accounts on {selected_platform}')
    # Streamlit render
    st.pyplot(fig)

def country_analysis(selected_Country):
    country = df[df['Country'] == selected_Country].groupby(['Country','Platform']).agg({
        'Daily Time Spent (min)': 'mean'
    })

    st.subheader('Country Average Time Spend On Platform')
    st.dataframe(country)
    # we count country_popularity and display

    st.subheader(f'Platform Popularity in {selected_Country}')

    # Count platform popularity in the selected country
    country_popularity = df[df['Country'] == selected_Country]['Platform'].value_counts()

    # Create pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(country_popularity, labels=country_popularity.index, autopct='%1.1f%%', startangle=90)
    ax.set_title(f'Platform Popularity in {selected_Country}')
    ax.axis('equal')  # Equal aspect ratio ensures the pie is a circle

    st.pyplot(fig)
    st.subheader('Verification Rate in {}'.format(selected_Country))

    # Count how many verified/unverified users in India
    verify_counts = df[df['Country'] == selected_Country]['Verified Account'].value_counts()

    # Colors for verified/unverified
    colors = ['#4CAF50', '#FFC107']  # green and amber

    # Create pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        verify_counts,
        labels=verify_counts.index,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        textprops={'fontsize': 10}
    )
    ax.set_title('Verification Rate ', fontsize=14, fontweight='bold')
    ax.axis('equal')  # Keep the pie chart circular

    st.pyplot(fig)
# Streamlit app setup

st.title('Social Media User Analysis')

option = st.sidebar.selectbox('Select an option', ['Platform', 'Country', 'Primary Usage', 'Daily Time Spent'])

if option == 'Platform':
    selected_platform = st.selectbox('Select a Platform', platforms)
    # Immediately run the function on selection (no button needed)
    platform_analysis(selected_platform)
elif option == 'Country':
    selected_Country = st.selectbox('Select a Country', country_list)
    #run function to display data (we pass selected countery to fun)
    country_analysis(selected_Country)
elif option == 'Primary Usage':
    st.info("Primary usage analysis is under development.")
else:
    st.info("Daily time spent analysis is under development.")
