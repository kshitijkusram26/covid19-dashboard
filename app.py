#Libraries

import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
import plotly.express as px 
from io import BytesIO

#LAYOUT
st.set_page_config(layout="wide",page_title="COVID-19 DASHBOARD", initial_sidebar_state="expanded")

#load data
@st.cache_data
def load_data():
    data= pd.read_csv("data/cleaned_owid-covid-data.csv")
    df=pd.DataFrame(data)
    df['date']=pd.to_datetime(df['date'])
    return df
df=load_data()

st.sidebar.title("Filter Data")
countries=st.sidebar.multiselect("Select Countries: ",sorted(df['location'].unique()),default=['India','United States','Brazil'])
start_date=st.sidebar.date_input("Start Date",df['date'].min())
end_date=st.sidebar.date_input("End Date",df['date'].max())

#filtered data
filtered_df=df[
    (df['location'].isin(countries))&
    (df['date']>=pd.to_datetime(start_date))&
    (df['date']<=pd.to_datetime(end_date))
]


#Download BUTTON
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="Download Filtered Data",
    data=convert_df(filtered_df),
    file_name='filtered_covid_data.csv',
    mime='text/csv'
)

#Title
st.markdown("<h1 style='text-align: centre; color: #00FFAA;'> COVID-19 Dashboard</h1>",unsafe_allow_html=True)
tab1,tab2,tab3=st.tabs([" Trends","Visual Analysis","Summary"])

with tab1:
    st.subheader("Trend of Total Cases Over Time")
    fig= px.line(filtered_df,x='date',y='total_cases',color='location',template='plotly_dark')
    st.plotly_chart(fig,use_container_width=True)

    st.subheader("Trend of Total Deaths Over Time")
    fig2=px.line(filtered_df,x='date',y='total_deaths',color='location',template='plotly_dark')
    st.plotly_chart(fig2,use_container_width=True)

with tab2:
    col1,col2=st.columns(2)
    with col1:
        st.subheader('Pie Chart- Total Cases Share')
        latest=filtered_df.sort_values('date').groupby('location').tail(1)
        pie_fig=px.pie(latest,values='total_cases',names='location',template='plotly_dark')
        st.plotly_chart(pie_fig)

    with col2:
        st.subheader("Stacked Bar- New cases & Deaths")
        stacked_df=filtered_df.groupby(['location']).agg([{'new_cases':'sum','new_deaths':'sum'}]).reset_index()
        stack_fig=px.bar(stacked_df,x='location',y=['new_cases','new_deaths'],barmode='stack',template='plotly_dark')
        st.plotly_chart(stack_fig)

    st.subheader("Heatmap")
    corr=filtered_df[['total_cases','total_deaths','new_cases','new_deaths']].corr()
    fig,ax=plt.subplots(figsize=(6,4))
    sns.heatmap(corr,annot=True,cmap='rocket',fmt='.2f',ax=ax)
    st.plotly(fig)

with tab3:
    st.subheader("Filtered Data Summary")
    st.dataframe(filtered_df[['date','location','toatl_cases','new_cases','new_deaths']].sort_values(by='date'))

st.markdown("-------------")
st.markdown(
    "<p style='text-align: centre: gray;>Thank You</p>",
    unsafe_allow_html=True
)




