import numpy as np

from PIL import Image


def coloring_cell(file_path_in, cords, size, color, width_line=0,
                  file_path_out=None):
    """функция для раскраски указанной ячейки сетки изображения"""
    if file_path_out is None:
        file_path_out = file_path_in

    pixels = np.array(Image.open(file_path_in))

    for x, y in cords:
        for i in range(y + width_line, y + size - width_line + 1):
            for j in range(x + width_line, x + size - width_line + 1):
                pixels[i][j] = np.array(color)

    Image.fromarray(pixels, 'RGB').save(file_path_out)


if __name__ == "__main__":
    coloring_cell('../mesh_of_warehouse/warehouse_meshed.png',
                  [(0, 0)],
                  10, (0, 0, 0), width_line=1)
