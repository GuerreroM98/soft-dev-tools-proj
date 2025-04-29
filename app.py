import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


st.header('Market of Vehicles for Sale')
st.write('filter the data below to see the vehicles listed')


df = pd.read_csv('vehicles_us.csv')


df['date_posted'] = pd.to_datetime(df['date_posted'])

df['model_year'] = df['model_year'].fillna(df.groupby('model')['model_year'].transform(lambda x: x.median()))

df['cylinders'] = df['cylinders'].fillna(df.groupby('model')['cylinders'].transform(lambda x: x.median()))

df['odometer'] = df['odometer'].fillna(df.groupby('condition')['odometer'].transform(lambda x: x.median()))

df['paint_color'] = df['paint_color'].fillna('unknown')

df['is_4wd'] = df['is_4wd'].fillna(0)

df['is_4wd'] = df['is_4wd'].astype(bool)

df['model_year'] = df['model_year'].astype(int)


model_choice = df['model'].unique()
selected_model = st.selectbox('Select a model', model_choice)
min_year, max_year = int(df['model_year'].min()), int(df['model_year'].max())
year_range = st.slider("Choose years", value=(min_year, max_year), min_value=min_year,max_value= max_year)
actual_range = list(range(year_range[0], year_range[1]+1))
df_filtered = df[ (df.model == selected_model) & (df.model_year.isin(list(actual_range)) )]

st.dataframe(df_filtered)

st.header('Histogram distribution of vehicle model by vehicle type')

fig6 = px.histogram(df, x='model', color='type',barmode='overlay',nbins=30, title='distribution showing model count per vehicle type')

st.plotly_chart(fig6)

st.write('Analyzing Histoplot distribution of vehicles by model and type')

def vehicle_age_category(x):
    if x<5: return '<5'
    elif  x>=5 and x<10: return '5-10'
    elif x>=10 and x<20: return '10-20'
    else: return '>20'

df['vehicle_age'] = 2025 - df['model_year']
df['vehicle_age_category'] = df['vehicle_age'].apply(vehicle_age_category)  
list_for_scatter = ['odometer','condition','transmission']

st.header('Scatter distribution vehicle price')
choice_for_scatter = st.selectbox('Price dependency on',list_for_scatter)
fig = px.scatter(df, x='price', y=choice_for_scatter, color ='vehicle_age_category',hover_data=['model'])
st.plotly_chart(fig)


st.write('Analyzing relationship between vehicle odometer value, condition and transmission to see how car prices vary according to age, usage, and transmission type')











