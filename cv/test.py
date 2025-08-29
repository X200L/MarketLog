import cv2
import numpy as np


def process_image(img):
    # grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary, cv2.RETR_LIST,
                                   cv2.CHAIN_APPROX_SIMPLE)

    result = np.ones((gray.shape[0], gray.shape[1], 3), dtype=np.uint8) * 255

    fill_mask = np.zeros_like(gray)

    # все замкнутые области синим
    for cnt in contours:
        cv2.drawContours(fill_mask, [cnt], -1, 255, -1)

    result[fill_mask == 255] = [255, 0, 0]

    result[binary == 255] = [0, 0, 255]

    cv2.imwrite('result_image.jpg', result)


process_image(cv2.imread('tg_image_1915246607.png'))
