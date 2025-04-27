import streamlit as st
from PIL import Image
import random
import time
from utils.image_processor import process_image
from utils.bbs import BlumBlumShub

st.header("⚖️ Compare Algorithms")
uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    seed = random.randint(1000, 9999)
    while True:
        try:
            bbs = BlumBlumShub(seed)
            p, q = bbs.p, bbs.q
            break
        except ValueError:
            seed = random.randint(1000, 9999)

    start_bbs = time.time()
    encrypted_bbs = process_image(image, seed, "BBS", p, q)
    bbs_time = time.time() - start_bbs

    start_lcg = time.time()
    encrypted_lcg = process_image(image, seed, "LCG")
    lcg_time = time.time() - start_lcg

    st.image(encrypted_bbs, caption=f"BBS Encrypted (Time: {bbs_time:.4f}s)")
    st.image(encrypted_lcg, caption=f"LCG Encrypted (Time: {lcg_time:.4f}s)")
    st.success("🏆 Faster Algorithm: " + ("BBS" if bbs_time < lcg_time else "LCG"))