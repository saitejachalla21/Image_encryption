import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from utils.robustness_tests import RobustnessMetrics as RM

st.title("🧪 Performance Analysis ")

orig_file = st.file_uploader("Upload Original Image", type=["png", "jpg", "jpeg"])
enc_file = st.file_uploader("Upload Encrypted Image", type=["png", "jpg", "jpeg"])
dec_file = st.file_uploader("Upload Decrypted Image", type=["png", "jpg", "jpeg"])

if orig_file and enc_file and dec_file:
    orig_img = np.array(Image.open(orig_file).convert("RGB"))
    enc_img = np.array(Image.open(enc_file).convert("RGB"))
    dec_img = np.array(Image.open(dec_file).convert("RGB"))

    st.subheader("📊 Baseline Metrics (Original vs Decrypted)")
    st.write(f"*PSNR:* {RM.compute_psnr(orig_img, enc_img):.2f} dB")
    st.write(f"*SSIM:* {RM.compute_ssim(orig_img, enc_img):.4f}")
    st.write(f"*SNR:* {RM.compute_snr(orig_img, enc_img):.2f} dB")
    st.write(f"*MSE:* {RM.compute_mse(orig_img, enc_img):.4f}")
    st.write(f"*RMSE:* {RM.compute_rmse(orig_img, enc_img):.4f}")
    st.write(f"*MAE:* {RM.compute_mae(orig_img, enc_img):.4f}")

    st.subheader("📈 Histogram & Correlation Analysis (Encrypted Image)")
    entropy_val = RM.compute_entropy(enc_img)
    h_corr, v_corr, d_corr = RM.correlation(enc_img)
    st.write(f"*Entropy:* {entropy_val:.4f}")
    st.write(f"*Correlation (H, V, D):* {h_corr:.4f}, {v_corr:.4f}, {d_corr:.4f}")

    # st.subheader("🧪 Differential Analysis (NPCR & UACI)")
    # modified = np.copy(enc_img)
    # i, j = np.random.randint(0, enc_img.shape[0]), np.random.randint(0, enc_img.shape[1])
    # modified[i, j, 0] = (modified[i, j, 0] + 1) % 256
    # npcr, uaci = RM.npcr_uaci(enc_img, modified)
    # st.write(f"*NPCR:* {npcr:.2f}% (Ideal ≈ 99%)")
    # st.write(f"*UACI:* {uaci:.2f}% (Ideal ≈ 33%)")
    

    st.subheader("🔁 Visual Robustness Tests (Attack Simulation)")
    st.image(RM.apply_noise(enc_img, "s&p"), caption="Noise Attack")
    st.image(RM.apply_compression(enc_img), caption="Compression Attack")
    st.image(RM.apply_crop(enc_img), caption="Cropping Attack")
    st.image(RM.apply_blur(enc_img), caption="Filtering (Blur) Attack")

    st.success("✅ All robustness tests complete.")

    st.subheader("📊 Final Robustness Summary")
    st.markdown(f"""
    *Evaluation Criteria:*

    

    - 📈 *Adjacent Pixel Correlation:*  
      A secure encrypted image should show low correlation between adjacent pixels.  
      - Measured by: *Horizontal, Vertical, Diagonal correlation ≈ 0*

    - 🎲 *Intensity Histogram (Entropy):*  
      A flat histogram indicates no visible patterns.  
      - Measured by: *High entropy (~7.99 for RGB images)*

    *Your Results:*

    - *Entropy:* {entropy_val:.4f} (Target: >7.5)
    - *Correlation (H, V, D):* {h_corr:.4f}, {v_corr:.4f}, {d_corr:.4f} (Target: near 0)
    """)

    st.subheader("📊 Intensity Histogram ")
    # fig, ax = plt.subplots()
    # color = ('r', 'g', 'b')
    # for i, col in enumerate(color):
    #     histr = cv2.calcHist([enc_img], [i], None, [256], [0, 256])
    #     ax.plot(histr, color=col)
    #     ax.set_xlim([0, 256])
    # ax.set_title("RGB Intensity Histogram")
    # ax.set_xlabel("Pixel Intensity")
    # ax.set_ylabel("Frequency")
    # st.pyplot(fig)
    if orig_img is not None and enc_img is not None:
    # Create a layout with two columns
      col1, col2 = st.columns(2)

    # Histogram of the Original Image
      with col1:
        st.subheader("Original Image")
        fig_orig, ax_orig = plt.subplots()
        color = ('r', 'g', 'b')
        for i, col in enumerate(color):
            histr = cv2.calcHist([orig_img], [i], None, [256], [0, 256])
            ax_orig.plot(histr, color=col)
            ax_orig.set_xlim([0, 256])
        ax_orig.set_title("RGB Intensity Histogram")
        ax_orig.set_xlabel("Pixel Intensity")
        ax_orig.set_ylabel("Frequency")
        st.pyplot(fig_orig)

    # Histogram of the Encrypted Image
      with col2:
        st.subheader("Encrypted Image")
        fig_enc, ax_enc = plt.subplots()
        color = ('r', 'g', 'b')
        for i, col in enumerate(color):
            histr = cv2.calcHist([enc_img], [i], None, [256], [0, 256])
            ax_enc.plot(histr, color=col)
            ax_enc.set_xlim([0, 256])
        ax_enc.set_title("RGB Intensity Histogram")
        ax_enc.set_xlabel("Pixel Intensity")
        ax_enc.set_ylabel("Frequency")
        st.pyplot(fig_enc)
   