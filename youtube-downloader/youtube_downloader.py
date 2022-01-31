import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from pytube import YouTube
from zipfile import ZipFile

st.set_page_config(page_title = "Youtube Downloader", page_icon = "🤖")   #layout="wide")

st.title('Youtube Downloader')

st.subheader("Enter the URL:")
url_video = st.text_input(label='URL')

yt = YouTube(url_video)

print(yt.streams)

if url_video != '':
    yt = YouTube(url_video)

    st.image(yt.thumbnail_url, width=300)
    
    st.subheader("Title : " + yt.title)
    
    st.text('''
    Length: {} seconds
    Rating: {} 
    '''.format(yt.length , yt.rating))

    video = yt.streams

    zip_file = ZipFile('video.zip', 'w')
    zip_file.write(video.get_lowest_resolution().download())
    #zip_file.write('yt.srt')
    zip_file.close()

    with open("video.zip", "rb") as zip_download:
        btn = st.download_button(
            label="Download VIDEO",
            data=zip_download,
            file_name="downloaded_video"
        )
