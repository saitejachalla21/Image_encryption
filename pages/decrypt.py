import streamlit as st
from PIL import Image
import io
from utils.image_processor import process_image

st.header("🔓 Decrypt Image")
uploaded_file = st.file_uploader("Upload Encrypted Image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    algo_choice = st.selectbox("Choose Algorithm:", ["BBS", "LCG"])
    seed = st.number_input("Enter Seed:", min_value=0, step=1)
    p = q = None
    if algo_choice == "BBS":
        p = st.number_input("Enter P:", min_value=0, step=1)
        q = st.number_input("Enter Q:", min_value=0, step=1)

    if st.button("Decrypt Image"):
        try:
            decrypted_image = process_image(image, int(seed), algo_choice, int(p) if p else None, int(q) if q else None)
            st.image(decrypted_image, caption="Decrypted Image")
            buffer = io.BytesIO()
            decrypted_image.save(buffer, format="PNG")
            buffer.seek(0)
            st.download_button("Download Decrypted Image", data=buffer, file_name="decrypted.png", mime="image/png")
        except Exception as e:
            st.error(f"Decryption failed: {e}")