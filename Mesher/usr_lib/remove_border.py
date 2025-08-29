import json
from PIL import Image


def remove_border(input_img, border_info):
    border = {}
    with open(border_info, 'r') as file:
        border = json.load(file)

    with Image.open(input_img) as img:
        w, h = img.size
        nl = border['left']
        nt = border['top']
        nr = w - border['right']
        nb = h - border['bottom']

        res_img = img.crop((nl, nt, nr, nb))

        return res_img
