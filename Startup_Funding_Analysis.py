import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Set the Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(layout='wide', page_title='Startup Analysis')

# Load data from the CSV file
df = pd.read_csv("startup_cleaned.csv")

# Sidebar title
st.sidebar.title("Startup Funding Analysis")

# Some changes in df
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year'] = df['date'].dt.year
df['month']= df['date'].dt.month

# General Analysis 



def load_overall_analysis():
    
    # Cards -> Total invested , Max , Avg , Total funded startups
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        
        # Total amount invested so far
        total_invested_amount = df['amount'].sum()
        st.metric('Total Funding' , str(int(total_invested_amount)) + ' Cr')
    
    with col2:
        
        # Maximum
        max_invested = max_invested = df.groupby('startup')['amount'].max().sort_values(ascending = False).head(1)
        st.metric('Max Funding', str(int(max_invested)) + ' Cr')
        
    with col3:
        
        # Avg funding of the startups
        avg_funding = df.groupby('startup')['amount'].sum().mean()
        st.metric('Avg Funding', str(int(avg_funding))+ ' Cr')


    with col4:
        
        #Total number of startup
        total_startup = df['startup'].nunique()
        st.metric('Total Startups', total_startup)
        
    # MoM chart -> Total + Count
    
    
        

# Function to load and display details about a selected investor
def load_investors_detail(investor):
    st.title(investor)
    
    # Display the most recent 5 investments made by the investor
    st.subheader('Most Recent Investments')
    recent_investments = df[df['investor'].str.contains(investor, case=False)].head()
    st.dataframe(recent_investments[['date', 'startup', 'vertical', 'city', 'round', 'amount']])
    
    col1, col2 = st.columns(2)
    
    # Biggest investments made by the investor
    with col1:
        st.subheader('Biggest Investments')
        big_investments = df[df['investor'].str.contains(investor, case=False)]
        if not big_investments.empty:
            big_series = big_investments.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.bar(big_series.index, big_series.values)
            st.pyplot(fig)
        else:
            st.write("No investment data available for this investor.")
    
    # Sectors the investor has invested in
    with col2:
        st.subheader('Sectors Invested In')
        if not big_investments.empty:
            sector_series = big_investments.groupby('vertical')['amount'].sum()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(sector_series.values, labels=sector_series.index, autopct='%1.1f%%')
            st.pyplot(fig)
        else:
            st.write("No sector data available for this investor.")
    
    col1, col2 = st.columns(2)
     
    # Funding Stage
    with col1:
        st.subheader('Funding Stage')
        if not big_investments.empty:
            stage_series = big_investments.groupby('round')['amount'].sum()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(stage_series.values, labels=stage_series.index, autopct='%1.1f%%')    
            st.pyplot(fig)
        else:
            st.write("No funding stage data available for this investor.")
    
    # City of investment
    with col2:
        st.subheader('City of Investment')
        if not big_investments.empty:
            city_series = big_investments.groupby('city')['amount'].sum()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.pie(city_series.values, labels=city_series.index, autopct='%1.1f%%')    
            st.pyplot(fig)
        else:
            st.write("No city data available for this investor.")
        
    col1, col2 = st.columns(2)
    with col1:
        st.header('YoY Investment')
        if not big_investments.empty:
            yoy_series = big_investments.groupby('year')['amount'].sum()
            fig, ax = plt.subplots(figsize=(8, 6))
            ax.plot(yoy_series.index, yoy_series.values, marker='o', linestyle='-')
            ax.set_xlabel('Year')
            ax.set_ylabel('Total Investment Amount')
            st.pyplot(fig)
        else:
            st.write("No year-over-year data available for this investor.")
        
  
# Sidebar option for user to select analysis type
option = st.sidebar.selectbox("Select Analysis Type", ['Overall Analysis', 'Startup', 'Investors'])

# Display content based on the selected analysis type
if option == 'Overall Analysis':
    st.title('Overall Analysis')
    btn0 = st.sidebar.button('Show Overall Analysis')
    
    if btn0:
        load_overall_analysis()
        

elif option == 'Startup':
    st.title("Startup Analysis")
    selected_startup = st.sidebar.selectbox("Select Startup", sorted(df['startup'].unique()))
    btn1 = st.sidebar.button("Find Startup Details")
    # Add functionality for showing details about the selected startup if btn1 is clicked

elif option == 'Investors':
    selected_investor = st.sidebar.selectbox("Select Investor", sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    
    # Display investor details if the button is clicked
    if btn2:
        load_investors_detail(selected_investor)


