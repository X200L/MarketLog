from PIL import Image


def add_borders(intput, output, left, right, top, bottom, size, color='red'):
    """функция добовляет к указанному изображению рамку
     и сохраняет в указанный файл"""

    image = Image.open(intput)

    width, height = image.size

    new_width = width + left + right + 2 * size
    new_height = height + top + bottom + 2 * size

    bordered_image = Image.new('RGB', (new_width, new_height), color)
    bordered_image.paste(image, (left + size, top + size))

    bordered_image.save(output)


if __name__ == "__main__":
    add_borders('../outline_of_warehouse/img2.png',
                '../outline_of_warehouse/img2.png',
                100, 100, 100, 100, 50, color='green')