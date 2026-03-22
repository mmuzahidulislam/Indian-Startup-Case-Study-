from email.policy import default

import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title='Startup Funding Analysis', page_icon=':bar_chart:', layout='wide')

# print investor details
def load_investor_details(investor):
    st.title(investor)
    # load the recent investment of the investor
    last5_df = df[df.investors.str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # Bigest investment of the investor
        i_max=df[df.investors.str.contains(investor)].groupby('startup').amount.sum().sort_values(ascending=False).head(5)
        st.subheader('Biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(i_max.index,i_max.values)
        st.pyplot(fig)
    with col2:
        # Investment by vertical
        vertical_series = df[df.investors.str.contains(investor)].groupby('vertical').amount.sum()
        st.subheader('Sector-wise Investment')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index,autopct='%1.1f%%')
        st.pyplot(fig1)

    col3, col4 = st.columns(2)
    with col3:
        # Investment by round
        round_series = df[df.investors.str.contains(investor)].groupby('round').amount.sum()
        st.subheader('Round-wise Investment')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series,labels=round_series.index,autopct='%1.1f%%')
        st.pyplot(fig2)

    with col4:
        # Investment by city
        city_series = df[df.investors.str.contains(investor)].groupby('city').amount.sum()
        st.subheader('City-wise Investment')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series,labels=city_series.index,autopct='%1.1f%%')
        st.pyplot(fig3)
    col5, col6 = st.columns(2)
    with col5:
        # Investment by year
        year_series = df[df.investors.str.contains(investor)].groupby('year').amount.sum()
        st.subheader('Year-wise Investment')
        fig4, ax4 = plt.subplots()
        ax4.plot(year_series.index, year_series.values, marker='o')
        st.pyplot(fig4)




# overviw analysis
def load_overview():
    st.title('Startup Funding Analysis - Overview')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
    #total invested amount
        total_investment = df['amount'].sum()
        st.metric(label='Total Investment', value=f'BDT   {total_investment:,.2f} Cr')
    with col2:
        max_amount=df.groupby('startup').amount.max().sort_values(ascending=False).head(1).values[0]
        st.metric(label='Biggest Investment', value=f'BDT   {max_amount:,.2f} Cr')
    with col3:
        average_ticket_size = round (df.groupby('startup').amount.sum().mean())
        st.metric(label='Average Ticket Size', value=f'BDT   {average_ticket_size:,.2f} Cr')

    with col4:
        total_startups = df['startup'].nunique()
        st.metric(label='Total Startups', value=total_startups)


    st.header('MOM Graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month']).amount.sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month']).amount.count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype(str) + '-' + temp_df['year'].astype(str)
    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'], marker='o')
    st.pyplot(fig5)


# Load the dataset
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year


st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overview', 'Investors', 'Startups'])

if option == 'Overview':
    load_overview()


elif option == 'Investors':
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn1 = st.sidebar.button('Find Investor Details')
    if btn1:
        load_investor_details(selected_investor)

elif option == 'Startups':
    st.sidebar.selectbox('Select Startup', df['startup'].unique().tolist())
    btn2 = st.sidebar.button('Find Startup Details')
    st.title('Startup Funding Analysis - Startups')

