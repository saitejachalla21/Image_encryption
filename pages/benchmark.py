import streamlit as st
from PIL import Image
import time
import random
import matplotlib.pyplot as plt
from utils.image_processor import process_image
from utils.bbs import BlumBlumShub

st.header("📊 Benchmark & Security Tips")
uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    sizes = [50, 100, 200, 400, 800]
    bbs_times, lcg_times = [], []
    seed = random.randint(1000, 9999)

    for size in sizes:
        resized = image.resize((size, size))
        while True:
            try:
                temp_bbs = BlumBlumShub(seed)
                p, q = temp_bbs.p, temp_bbs.q
                break
            except ValueError:
                seed = random.randint(1000, 9999)

        start = time.time()
        process_image(resized, seed, "BBS", p, q)
        bbs_times.append(time.time() - start)

        start = time.time()
        process_image(resized, seed, "LCG")
        lcg_times.append(time.time() - start)

    fig, ax = plt.subplots()
    ax.plot(sizes, bbs_times, label="BBS", marker="o")
    ax.plot(sizes, lcg_times, label="LCG", marker="s")
    ax.set_xlabel("Image Size")
    ax.set_ylabel("Time (s)")
    ax.set_title("Encryption Time vs Image Size")
    ax.legend()
    st.pyplot(fig)

    st.subheader("🔐 Security Comparison Tips:")
    st.markdown("""
- *BBS*: Stronger randomness and security but slower.
- *LCG*: Fast but predictable.
- Prefer BBS for secure applications.
- Use LCG when speed is more critical than security.
    """)