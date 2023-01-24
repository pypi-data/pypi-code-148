"""W module to collect a variety of image processing 
functions and """
from datetime import datetime
import logging
import cv2
import numpy as np

from scipy.ndimage import interpolation

logger = logging.getLogger(__name__)

def mean_squared_error(img1: np.array, img2: np.array):
    """caclulated the mean square error for
    2 images"""
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse, diff

def anglescore(img: np.array, angle: int = 1):
    """Calculates the score for the image,
    it return the value with the hightest horizontal
    pixels"""
    data = interpolation.rotate(img, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score

def bestangle(img: np.array, limit: int = 10, step: int = 1, thresh: int = 100) -> dict:
    """Uses the historgram method to minimize the 
    vertical and horizotal values.
    uses the limit and step to roate the image to 
    img: raw image, converted to binary, 1 = pixel, 0 = below threshold
    """
    workimging = img.copy()
    h, w, c = img.shape
    if c > 1:
        # convert to gray scale
        img = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

    # turn gray scale
    (thresh, img_bw) = cv2.threshold(src=img, thresh=thresh, maxval=255, type=cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # get the bext angle
    scores = []
    angles = range(-limit, limit + step, step)
    logger.debug("angles: %s", angles)
    for angle in angles:
        hist, score = anglescore(img=img_bw, angle=angle)
        scores.append(score)
    logger.debug("scores: %s", scores)

    return angles[scores.index(max(scores))]
