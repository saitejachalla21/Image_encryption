import streamlit as st
from PIL import Image
import random
import io
from utils.image_processor import process_image
from utils.bbs import BlumBlumShub

st.header("🔒 Encrypt Image")
uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    algo_choice = st.selectbox("Choose Algorithm:", ["BBS", "LCG"])

    if algo_choice == "BBS":
        while True:
            seed = random.randint(1000, 9999)
            try:
                temp_bbs = BlumBlumShub(seed)
                p, q = temp_bbs.p, temp_bbs.q
                break
            except ValueError:
                continue
        encrypted_image = process_image(image, seed, "BBS", p, q)
        st.image(encrypted_image, caption="Encrypted using BBS")
        st.code(f"Seed: {seed}\nP: {p}\nQ: {q}")
    else:
        seed = random.randint(1000, 9999)
        encrypted_image = process_image(image, seed, "LCG")
        st.image(encrypted_image, caption="Encrypted using LCG")
        st.code(f"Seed: {seed}")

    buffer = io.BytesIO()
    encrypted_image.save(buffer, format="PNG")
    buffer.seek(0)
    st.download_button("Download Encrypted Image", data=buffer, file_name="encrypted.png", mime="image/png")