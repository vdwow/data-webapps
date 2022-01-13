import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(layout="wide")

DATA = ('https://raw.githubusercontent.com/vdwow/data-scraping/master/data_exported/GDPR_FINES.csv')

@st.cache

def load_data(nrows):
    data = pd.read_csv(DATA, nrows=nrows)
    data = data.drop(['Unnamed: 0', 'Source'], axis = 1)
    data.columns = ['ID', 'Country', 'Date', 'Amount in €', 'Fined Company', 'GDPR Articles violated',' Type of infraction']
    
    data['ID'] = data['ID'].str.replace('ETid-', '')
    
    data['Date'] = data['Date'].str.replace('Unknown', '2018-06-01')

    data['Fined Company'] = data['Fined Company'].str.upper()
    
    data['Amount in €'] = data['Amount in €'].str.replace(',','').str.replace('Unknown','0').str.replace('Only intention to issue fine','0')
    data['Amount in €'] = data['Amount in €'].astype('int')

    return data


def main():

    st.title('Historic of GDPR fines since May 2018')
    #st.write("Parking Spot Vacancy with Machine Learning")

    # Render the readme as markdown using st.markdown as default
    #readme_text = st.markdown(get_file_content_as_string("instructions.md"))

     # Once we have the dependencies, add a selector for the app mode on the sidebar.
    #data_load_state = st.text('Loading data...')
    data = load_data(10000)
    
    st.sidebar.title("Settings")

    app_mode = st.sidebar.selectbox("Choose the app mode",
        ["Home", "Top Fives"])
    
    if app_mode == "Home":

        # Notify the reader that the data was successfully loaded.
        #data_load_state.text("Loading done! (using streamlit cache)")
        st.text("Since GDPR went into effect in May 2018, European local authorities have begun work on financial penalties for companies that do not comply with the principles of this regulation. Let's explore the GDPR fines of the past few years!")
        st.subheader('Last 5 fines to date : ' + str(date.today()))
        st.write(data.head(5))

        st.sidebar.success('You can navigate through many KPIs over here !')
    
    elif app_mode == "Top Fives":

        st.subheader('Top 5 biggest fines')
        st.write(data.sort_values(by = "Amount in €", ascending = False).head(5))
        
        col1, col2, col3, col4 = st.columns(4)

        col1.subheader('Top 5 countries with most fines')
        col1.write(data.groupby('Country').count()['ID'].sort_values(ascending = False).head(5))

        col2.subheader('Top 5 countries with most value out of fines')
        col2.write(data.groupby('Country').sum()['Amount in €'].sort_values(ascending = False).head(5))   

        col3.subheader('Top 5 countries with biggest mean fine value')
        col3.write(data.groupby('Country').mean()['Amount in €'].sort_values(ascending = False).head(5)) 

        col4.subheader('Top 5 countries with smallest mean fine value')
        col4.write(data.groupby('Country').sum()['Amount in €'].sort_values(ascending = True).head(5))


#df_top_types = df.groupby('Type').agg({'ID':'count','Amount':'sum'}).sort_values(by = 'ID', ascending = False)
#df_top_types.columns = ['Total_volume','Total_amount_euros']
#df_top_types.head(3)
#df_top_types

    return None

main()
