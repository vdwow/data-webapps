import streamlit as st
import pandas as pd
import numpy as np

st.title('TEST BADOMATIC')

DATA = ('https://raw.githubusercontent.com/vdwow/data-scraping/master/gdpr_fines/data_enforcment.csv')

@st.cache

def load_data(nrows):
    data = pd.read_csv(DATA, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)
    #data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(1000)
# Notify the reader that the data was successfully laoded.
data_load_state.text("Done! (using st.cache)")


#data preparation
data = data.drop('Unnamed: 0', axis = 1)

data['Amount'] = data['Amount'].str.replace(' ','').str.replace(r'[a-zA-Z,]','').replace(r'^\s*$', 0, regex=True)
data['Amount'] = data['Amount'].astype(int)


st.subheader('Overview of raw data')
st.write(data.head(5))

st.subheader('Top 5 fines !')
top_5_fines = data.sort_values(by='Amount', ascending = False)[['Controller_Processor','Amount', 'Date']].head()
st.write(top_5_fines)
