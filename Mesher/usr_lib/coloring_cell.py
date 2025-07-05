import numpy as np

from PIL import Image


def coloring_cell(file_path, x, y, size, color, width_line=0):
    """функция для раскраски указанной ячейки сетки изображения"""

    pixels = np.array(Image.open(file_path))
    for i in range(y + width_line, y + size - width_line + 1):
        for j in range(x + width_line, x + size - width_line + 1):
            pixels[i][j] = np.array(color)

    Image.fromarray(pixels, 'RGB').save(file_path)


if __name__ == "__main__":
    coloring_cell('Mesher/mesh_of_warehouse/warehouse_meshed.png',
                  0, 0,
                  10, (0, 100, 100), width_line=1)
