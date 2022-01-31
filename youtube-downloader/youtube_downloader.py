import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from pytube import YouTube

/home/appuser/venv/bin/python -m pip install --upgrade pip

st.set_page_config(page_title = "Youtbe Downloader", page_icon = "random")   #layout="wide")

st.title('Youtube Downloader')

st.subheader("Enter the URL:")
url_video = st.text_input(label='URL')

yt = YouTube(url_video)

print(yt.streams)

if url != '':
    yt = YouTube(url)
    st.image(yt.thumbnail_url, width=300)
    
    st.subheader("Title : " + yt.title)
    
    st.text('''
    Length: {} seconds
    Rating: {} 
    '''.format(yt.length , yt.rating))

    video = yt.streams

    if len(video) > 0:
        downloaded , download_audio = False , False
        download_video = st.button("Download Video")
        if yt.streams.filter(only_audio=True):
            download_audio = st.button("Download Audio Only")
        if download_video:
            video.get_lowest_resolution().download()
            downloaded = True
        if download_audio:
            video.filter(only_audio=True).first().download()
            downloaded = True
        if downloaded:
            st.subheader("Download Complete")
    else:
        st.subheader("Sorry, this video can not be downloaded")
