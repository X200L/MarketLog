import sys
import numpy as np

from PIL import Image, ImageDraw
from Mesher.usr_lib.coloring_cell import coloring_cell
from Mesher.usr_lib.create_graph import create_graph


def prepare_matrix(matrix):
    matrix = np.array(matrix)
    matrix = np.pad(matrix, pad_width=2, constant_values=-3)

    size = 30
    width_line = 1
    new_image = Image.new('RGB', ((len(matrix[0]) * size),
                                  (len(matrix) * size)), color=(255, 0, 0))

    vertex = set()
    oz = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] not in {-3, -2}:
                vertex.add((i, j))

            if matrix[i][j] == -1:
                oz.append((i, j))

    graph = create_graph(vertex, (oz[0]))
    for e in oz:
        if e not in graph:
            print("Операционные зоны находятся в разных компонентах связности!")
            sys.exit()

    new_image = np.array(new_image)
    for ky in range(len(matrix)):
        for kx in range(0, len(matrix[0])):
            if (ky, kx) in graph:
                for x_cell in range(size * ky, size * (ky + 1)):
                    for y_cell in range(size * kx, size * (kx + 1)):
                        new_image[x_cell][y_cell] = np.array((0, 255, 0))

            if matrix[ky][kx] == -1:
                oz.append((ky, kx))

    (Image.fromarray(new_image, 'RGB').
     save('../tmp_photo/coloring_warehouse.png'))

    image = Image.open('../tmp_photo/coloring_warehouse.png')
    draw = ImageDraw.Draw(image)

    for x_cell in range(0, len(matrix[0]) * size, size):
        if 0 <= x_cell < len(matrix[0]) * size:
            draw.line((x_cell, 0, x_cell, len(matrix) * size),
                      fill=(0, 0, 0), width=width_line)

    for y_cell in range(0, len(matrix) * size, size):
        if 0 <= y_cell < len(matrix) * size:
            draw.line((0, y_cell, len(matrix[0]) * size, y_cell),
                      fill=(0, 0, 0), width=width_line)

    image.save('../tmp_photo/warehouse_meshed.png')
    coloring_cell('../tmp_photo/warehouse_meshed.png',
                  [(operation_zone_x * size, operation_zone_y * size)
                   for operation_zone_y, operation_zone_x in oz],
                  size, color=(0, 100, 100), width_line=width_line)

    img_copy = Image.open('../tmp_photo/warehouse_meshed.png')
    for i in range(0, 6):
        img_copy.save(f'../tmp_photo/warehouse_roads{i}.png')
    img_copy.close()

    return matrix, size, width_line


if __name__ == "__main__":
    m = [[0, -3, -3, -3, -3, -3, -3, -3, 0],
         [-3, -3, -3, 0, 0, 0, -3, 0, -3],
         [-3, -3, 0, 0, 0, 0, 0, -3, -3],
         [-3, 0, 0, 0, 0, 0, 0, 0, -3],
         [-3, 0, 0, 0, 0, 0, 0, 0, -3],
         [-3, 0, 0, 0, 0, 0, 0, 0, -3],
         [-3, -3, 0, 0, 0, 0, -1, -3, -3],
         [-3, -3, -3, 0, -1, 0, -3, -3, -3],
         [0, -3, -3, -3, -3, -3, -3, -3, 0]]

    prepare_matrix(m)
