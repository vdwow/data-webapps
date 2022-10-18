import streamlit as st

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

from PIL import Image

# Create streamlit app

st.title('Stable bud')

modelid = "CompVis/stable-diffusion-v1-4"
device = "cuda"

pipe = StableDiffusionPipeline.from_pretrained(modelid, revision="fp16", torch_dtype=torch.float16, use_auth_token="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") 

pipe.to(device) 

def generate(): 
    with autocast(device):
        
        image = pipe(user_input, guidance_scale=8.5)["sample"][0]
    
    image.save('generatedimage.png')


user_input = st.text_input('Input your text here...')

if st.button('Generate'):
    st.write('Image generation...')
    generate()
    st.image('generatedimage.png')

else:
    st.text('Click the button to generate image.')