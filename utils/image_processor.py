import numpy as np
from PIL import Image
from utils.bbs import BlumBlumShub
from utils.lcg import LCG

def process_image(image, seed, algorithm="BBS", p=None, q=None):
    rng = BlumBlumShub(seed, p, q) if algorithm == "BBS" else LCG(seed)
    pixels = np.array(image.convert('RGB'))
    processed_pixels = np.zeros_like(pixels)

    rows, cols, channels = pixels.shape
    for i in range(rows):
        for j in range(cols):
            for c in range(channels):
                rand = rng.next()
                processed_pixels[i, j, c] = pixels[i, j, c] ^ rand

    return Image.fromarray(processed_pixels)