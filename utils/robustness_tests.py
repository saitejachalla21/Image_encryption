import numpy as np
import cv2
from skimage.metrics import structural_similarity as ssim
from scipy.stats import entropy

class RobustnessMetrics:

    @staticmethod
    def compute_mse(original, encrypted):
        return np.mean((original.astype("float") - encrypted.astype("float")) ** 2)

    @staticmethod
    def compute_rmse(original, encrypted):
        return np.sqrt(RobustnessMetrics.compute_mse(original, encrypted))

    @staticmethod
    def compute_mae(original, encrypted):
        return np.mean(np.abs(original.astype("float") - encrypted.astype("float")))

    @staticmethod
    def compute_psnr(original, encrypted):
        return cv2.PSNR(original, encrypted)

    @staticmethod
    def compute_snr(original, encrypted):
        signal_power = np.mean(original.astype("float") ** 2)
        noise_power = np.mean((original.astype("float") - encrypted.astype("float")) ** 2)
        if noise_power == 0:
            return float('inf')
        return 10 * np.log10(signal_power / noise_power)

    @staticmethod
    def compute_ssim(original, encrypted):
        return ssim(original, encrypted, channel_axis=-1, win_size=3)

    @staticmethod
    def compute_entropy(image):
        histogram = np.histogram(image.flatten(), bins=256)[0]
        histogram = histogram / np.sum(histogram)
        return entropy(histogram)

    @staticmethod
    def correlation(img):
        img = img.astype('float')
        h_corr = np.corrcoef(img[:, :-1].flatten(), img[:, 1:].flatten())[0, 1]
        v_corr = np.corrcoef(img[:-1, :].flatten(), img[1:, :].flatten())[0, 1]
        d_corr = np.corrcoef(img[:-1, :-1].flatten(), img[1:, 1:].flatten())[0, 1]
        return h_corr, v_corr, d_corr

    @staticmethod
    def npcr_uaci(img1, img2):
        diff = img1 != img2
        npcr = np.sum(diff) / diff.size * 100
        uaci = np.sum(np.abs(img1.astype(int) - img2.astype(int))) / (255 * diff.size) * 100
        return npcr, uaci

    @staticmethod
    def apply_noise(image, noise_type="s&p", amount=0.02):
        output = np.copy(image)
        if noise_type == "s&p":
            num_salt = np.ceil(amount * image.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
            output[tuple(coords)] = 255

            num_pepper = np.ceil(amount * image.size * 0.5)
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
            output[tuple(coords)] = 0

        elif noise_type == "gaussian":
            gauss = np.random.normal(0, 25, image.shape).astype('uint8')
            output = cv2.add(image, gauss)

        return output

    @staticmethod
    def apply_compression(image, quality=30):
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
        _, enc_img = cv2.imencode('.jpg', image, encode_param)
        return cv2.imdecode(enc_img, 1)

    @staticmethod
    def apply_blur(image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    @staticmethod
    def apply_crop(image, crop_ratio=0.1):
        h, w = image.shape[:2]
        ch, cw = int(h * crop_ratio), int(w * crop_ratio)
        cropped = image[ch:h - ch, cw:w - cw]
        return cv2.resize(cropped, (w, h))

