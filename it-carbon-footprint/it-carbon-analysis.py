import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

st.set_page_config(layout="wide")

st.title('Carbon IT footprint')

uploaded_file = st.file_uploader("Import a file :")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, sep=";")
    st.write(df)
    print(df.head)