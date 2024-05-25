import streamlit as st
st.title("Image, Audio and video")


#Image
from PIL import Image
img = Image.open("image.jpg")
st.image(img)
st.image(img, width = 300, caption = "This is Image")


# Video
vid_file = open("video.mp4", "rb")
vid_bytes = vid_file.read()
st.video(vid_bytes)


# Audio
sudio_file = open("audio.m4a", "rb").read()
st.audio(sudio_file)