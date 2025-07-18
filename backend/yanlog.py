import cv2
import numpy as np
import os

def thicken_and_color_image(img, max_distance=3, thickness=2):
    if len(img.shape) > 2:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    kernel_size = max_distance * 2 + 1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    connected = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    if thickness > 1:
        thick_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (thickness, thickness))
        connected = cv2.dilate(connected, thick_kernel, iterations=1)
    contours, _ = cv2.findContours(connected, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    result = np.ones((gray.shape[0], gray.shape[1], 3), dtype=np.uint8) * 255
    fill_mask = np.zeros_like(connected)
    for cnt in contours:
        cv2.drawContours(fill_mask, [cnt], -1, 255, -1)
    result[fill_mask == 255] = [255, 0, 0]
    result[connected == 255] = [0, 0, 255]
    return result

class ImageProcessor:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder

    def process_file(self, path, filename):
        filepath = os.path.join(self.upload_folder, path+'/'+filename)
        img = cv2.imread(filepath)
        if img is None:
            raise FileNotFoundError(f"File not found: {filepath}")
        result = thicken_and_color_image(img, max_distance=3, thickness=2)
        processed_filename = f"{path}/processed_{filename}"
        processed_path = os.path.join(self.upload_folder, processed_filename)
        cv2.imwrite(processed_path, result)
        return processed_filename