import numpy as np
import os

from PIL import ImageDraw, Image
from backend.add_borders import add_borders
from backend.create_graph import create_graph
from backend.coloring_cell import coloring_cell
from backend.search_bfs import search_bfs


def mesh_function(image_path, operation_zone_x, operation_zone_y,
                  size=10, color_cell="black", width_line=1, epsilon=0.00, temp_upload_folder=None):
    # функция для разбиения схемы склада рабочие области

    """функция возвращает изменённую фотографию и
    список абсолютных координат рабочих областей"""
    print(12)

    if temp_upload_folder is None:
        temp_upload_folder = '../tmp_photo'
    image = Image.open(image_path)

    offset_x = operation_zone_x % size
    offset_y = operation_zone_y % size
    width, height = image.size

    left = size - offset_x
    right = size - ((width + left) % size)
    top = size - offset_y
    bottom = size - ((height + top) % size)
    offset_x += size
    offset_y += size

    add_borders(image_path, os.path.join(temp_upload_folder, 'bordered_image.png'),
                left, right, top, bottom, size)

    pixels = np.array(Image.open(os.path.join(temp_upload_folder, 'bordered_image.png')))

    height += top + bottom + 2 * size
    width += left + right + 2 * size
    offset_x += left
    offset_y += top

    cell_top = height // size
    cell_width = width // size

    vertex = []
    wall_vertex = []

    for ky in range(0, cell_top + 1):
        for kx in range(0, cell_width + 1):
            cell_middle_color = np.array([0, 0])
            for x_cell in range(size * (ky - 1), size * ky):
                for y_cell in range(size * (kx - 1), size * kx):
                    if pixels[x_cell][y_cell][0] >= pixels[x_cell][y_cell][2]:
                        cell_middle_color[0] += 1
                    else:
                        cell_middle_color[1] += 1

            if cell_middle_color[1] / (cell_middle_color[0] +
                                       cell_middle_color[1]) >= 1 - epsilon:
                vertex.append((kx, ky))
            else:
                wall_vertex.append((kx, ky))

            for x_cell in range(size * (ky - 1), size * ky):
                for y_cell in range(size * (kx - 1), size * kx):
                    pixels[x_cell][y_cell] = np.array((255, 0, 0))

    graph = create_graph(vertex, ((operation_zone_x + left) // size,
                                  (operation_zone_y + top) // size))

    wall_graph = create_graph(wall_vertex, (0, 0))
    print(74)

    for ky in range(0, cell_top + 1):
        for kx in range(0, cell_width + 1):
            if (kx, ky) in graph:
                for x_cell in range(size * (ky - 1), size * ky):
                    for y_cell in range(size * (kx - 1), size * kx):
                        pixels[x_cell][y_cell] = np.array((0, 255, 0))
    print(84)

    (Image.fromarray(pixels, 'RGB').
     save(os.path.join(temp_upload_folder, 'coloring_warehouse.png')))

    image = Image.open(os.path.join(temp_upload_folder, 'coloring_warehouse.png'))
    draw = ImageDraw.Draw(image)

    print(90)

    for x_cell in range(offset_x - size, width, size):
        if 0 <= x_cell < width:
            draw.line((x_cell, 0, x_cell, height),
                      fill=color_cell, width=width_line)

    for y_cell in range(offset_y - size, height, size):
        if 0 <= y_cell < height:
            draw.line((0, y_cell, width, y_cell),
                      fill=color_cell, width=width_line)
    print(101)

    image.save(os.path.join(temp_upload_folder, 'warehouse_meshed.png'))
    coloring_cell(os.path.join(temp_upload_folder, 'warehouse_meshed.png'),
                  [(operation_zone_x + left - size, operation_zone_y + top
                    - size)], size, color=(0, 100, 100), width_line=width_line)

    print(108)

    # -3 - стена
    # -2 - внутреннее препятствие
    # -1 - стартовая зона
    #  0 - пустая ячейка
    #  1 - ячейка хранения
    #  2 - зона поворота
    #  3 - зарядка
    #  4 - дороги

    matrix_const = np.array(
        [[-2 for _ in range(cell_width)] for _ in range(cell_top)])

    for i in search_bfs(wall_graph, (0, 0)):
        matrix_const[i[1] - 1][i[0] - 1] = -3

    ozy_cell = (operation_zone_y + top) // size - 1
    ozx_cell = (operation_zone_x + left) // size - 1
    print(127)

    for i in graph:
        matrix_const[i[1] - 1][i[0] - 1] = 0
    matrix_const[ozy_cell][ozx_cell] = -1

    img_copy = Image.open(os.path.join(temp_upload_folder, 'warehouse_meshed.png'))
    for i in range(0, 6):
        img_copy.save(os.path.join(temp_upload_folder, f'warehouse_roads{i}.png'))
    img_copy.close()
    print(137)

    return matrix_const, size, width_line


if __name__ == "__main__":
    mesh_function('../outline_of_warehouse/img4.png',
                  400, 300, 30)