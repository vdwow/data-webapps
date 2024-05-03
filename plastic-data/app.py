import streamlit as st
import pandas as pd

df_input = pd.read_csv('data/opendata-po-2022-fr.csv')

df_filtered = df_input.copy()

st.title('Maquette - accès données PO')

##
st.write('Apercu des données disponibles :')
st.dataframe(df_input.head())


st.header('Filtres à appliquer')

###

date_min = st.date_input('Date de début')
date_max = st.date_input('Date de fin')

##

rivers = st.multiselect('Sélectionnez les rivières souhaitées :', df_input['river_name'].unique())

##

banks = st.radio('Quelles rives ont été scannées ?', ['gauche', 'droite', 'les deux'])

##

#filtering

df_filtered['date_clean'] = df_filtered['date'].str[0:10].str.replace('-', '/')
df_filtered = df_filtered[(df_filtered['date_clean'] >= str(date_min)) & (df_filtered['date_clean'] <= str(date_max))]

df_filtered = df_filtered[df_filtered['river_name'].isin(rivers)]

df_filtered = df_filtered[df_filtered['bank']]

##

st.header('Téléchargement')

type_envoi = st.radio('Choisissez le type de données :', ['données brutes (.csv)', 'dataviz'])

#envoi email
envoi_email = st.toggle('Envoyez moi également par email ma sélection')

if envoi_email == True:
    
    st.text_input('Renseignez votre adresse email :')

def convert_df(df):
    return df.to_csv().encode("utf-8")

csv = convert_df(df_filtered)
    
if type_envoi == 'dataviz':
    st.write('dataviz à paramétrer')
    # with open("flower.png", "rb") as file:
    #     btn = st.download_button(
    #             label="Download image",
    #             data=file,
    #             file_name="flower.png",
    #             mime="image/png"
    #         )
else:
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name="export-plastic-origins.csv",
    mime="text/csv",
)