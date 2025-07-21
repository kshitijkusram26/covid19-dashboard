#Libraries

import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 




data= pd.read_csv("data\\cleaned_owid-covid-data.csv")
df=pd.DataFrame(data)
df['date']=pd.to_datetime(df['date'])
st.title(" COVID 19 Dashboard (Matplotlib & Seaborn)")
st.sidebar.header("Filter the Data")

country=st.sidebar.selectbox("Select Country",df['location'].unique())
date_range=st.sidebar.slider("Date Range",
                             min_value=df['date'].min().date(),
                             max_value=df['date'].max().date(),
                             value=(df['date'].min().date(), df['date'].max().date()))

df_country=df[(df['location']==country) & 
              (df['date']>=pd.to_datetime(date_range[0])) &
               (df['date']<=pd.to_datetime(date_range[1]))]

latest = df_country[df_country['date'] == df_country['date'].max()]





#KPI
st.metric("Total cases",int(latest['total_cases'].values[0]))
st.metric('Toatal Deaths',int(latest['total_deaths'].values[0]))
vaccinated = latest['people_vaccinated'].values[0]
if pd.notna(vaccinated):
    st.metric('People Vaccinated', int(vaccinated))
else:
    st.metric('People Vaccinated', "Data not available")


#Line Plot
st.subheader(f'New Daily Cases in{country}')
plt.figure(figsize=(12,8))
plt.plot(df_country['date'],df_country['new_cases'],color='green')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot()


st.subheader(f'Top 10 Countries by total COVID 19 cases')
top_10=df.groupby('location')['total_cases'].max().sort_values(ascending=False).head(10)
plt.figure(figsize=(12,8))
sns.barplot(x=top_10.values, y=top_10.index,palette='Reds_r',hue=None,legend=False)
plt.xlabel("Total Cases")
plt.tight_layout()
st.pyplot()


