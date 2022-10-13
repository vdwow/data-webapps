import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

st.set_page_config(layout="wide")

data_ref = 'https://raw.githubusercontent.com/Boavizta/environmental-footprint-data/main/boavizta-data-fr.csv'
ref_df = pd.read_csv(data_ref, sep = ';', error_bad_lines=False)
ref_df = ref_df[['manufacturer', 'name', 'gwp_total', 'yearly_tec', 'lifetime', 'use_location']]

ref_df['gwp_total'] = ref_df['gwp_total'].fillna(value = '0')
ref_df['gwp_total'] = ref_df['gwp_total'].str.replace(',', '').astype('int')/10

ref_df['lifetime'] = ref_df['lifetime'].fillna(value = '0')
ref_df['lifetime'] = ref_df['lifetime'].str.replace(',', '').astype('int')/10

ref_df['yearly_tec'] = ref_df['yearly_tec'].fillna(value = '0')
ref_df['yearly_tec'] = ref_df['yearly_tec'].str.replace(',', '').astype('int')/10

st.title('💻 Carbon IT footprint calculator 🍃')

uploaded_file = st.file_uploader("Import a file :")

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)
    st.text('First lines of loaded file :')
    st.write(df.head())

#df_grouped = df.groupby('model').agg({'id':['count']})
#st.write(df_grouped)

df = df.head()[['brand', 'model', 'volume']]

st.markdown("""---""")

st.text('Please help us mapping the data : ')

df['model'][0] = st.selectbox('Item 1 : ' + df['model'][0], ref_df[ref_df['manufacturer'] == df['brand'][0]]['name'].to_list())
df['model'][1] = st.selectbox('Item 2 : ' + df['model'][1], ref_df[ref_df['manufacturer'] == df['brand'][1]]['name'].to_list())
df['model'][2] = st.selectbox('Item 3 : ' + df['model'][2], ref_df[ref_df['manufacturer'] == df['brand'][2]]['name'].to_list())
df['model'][3] = st.selectbox('Item 4 : ' + df['model'][3], ref_df[ref_df['manufacturer'] == df['brand'][3]]['name'].to_list())
df['model'][4] = st.selectbox('Item 5 : ' + df['model'][4], ref_df[ref_df['manufacturer'] == df['brand'][4]]['name'].to_list())

df = df.merge(ref_df, left_on = 'model', right_on='name')

st.text(df.head())

###
df['gwp_mult'] = df['volume'] * df['gwp_total']
gwp_total = int(df['gwp_mult'].sum() / 1000)

###

df['scope_2'] = df['yearly_tec'] * df['lifetime'] * df['volume'] * 0.15
scope2_total = int(df['scope_2'].sum() / 1000)

###

df['scope_3'] = df['gwp_mult'] - df['scope_2']
scope3_total = int(df['scope_3'].sum() / 1000)

###

col1, col2, col3 = st.columns(3)

with col1:
   st.metric(label="GWP Total (teq)", value= gwp_total)

with col2:
   st.metric(label="Scope 2 Total (teq)", value= scope2_total)

with col3:
      st.metric(label="Scope 3 Total (teq)", value= scope3_total)



# for model in df.head()['model']:
    
#     dic_temp = {}
    
#     for ref in ref_df['name']:
        
#         dic_temp[ref] = fuzz.ratio(model, ref)
    
#     st.text(model)
#     st.text(max(dic_temp, key = dic_temp.get))
#     st.text('#################################')
    
    # st.text(model)
    # st.text(max(l))
    # st.text(l)