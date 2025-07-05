from PIL import Image


def add_borders(intput, output, left, right, top, bottom, color='red'):
    """функция добовляет к указанному изображению рамку
     и сохраняет в указанный файл"""

    image = Image.open(intput)

    width, height = image.size

    new_width = width + left + right
    new_height = height + top + bottom

    bordered_image = Image.new('RGB', (new_width, new_height), color)
    bordered_image.paste(image, (left, top))

    bordered_image.save(output)


if __name__ == "__main__":
    add_borders('Mesher/outline_of_warehouse/image.jpeg',
                "Mesher/test_border_function.png",
                100, 100, 100, 100, color='green')
