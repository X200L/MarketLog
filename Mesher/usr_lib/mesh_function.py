import numpy as np

from PIL import ImageDraw, Image
from Mesher.usr_lib.add_borders import add_borders
from Mesher.usr_lib.create_graph import create_graph
from Mesher.usr_lib.coloring_cell import coloring_cell
from Mesher.usr_lib.bfs import bfs


def mesh_function(image_path, operation_zone_x, operation_zone_y,
                  size=10, color_cell="black", width_line=1, epsilon=0.00):
    # функция для разбиения схемы склада рабочие области

    """функция возвращает изменённую фотографию и
    список абсолютных координат рабочих областей"""

    image = Image.open(image_path)

    offset_x = operation_zone_x % size
    offset_y = operation_zone_y % size
    width, height = image.size

    left = size - offset_x
    right = size - ((width + left) % size)
    top = size - offset_y
    bottom = size - ((height + top) % size)

    add_borders(image_path, '../tmp_photo/bordered_image.png',
                left, right, top, bottom)

    pixels = np.array(Image.open('../tmp_photo/bordered_image.png'))

    height += top + bottom
    width += left + right
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
                vertex.append((kx - 1, ky - 1))
            else:
                wall_vertex.append((kx - 1, ky - 1))

            for x_cell in range(size * (ky - 1), size * ky):
                for y_cell in range(size * (kx - 1), size * kx):
                    pixels[x_cell][y_cell] = np.array((255, 0, 0))

    graph = create_graph(vertex, ((operation_zone_x + left) // size,
                                  (operation_zone_y + top) // size))

    wall_graph = create_graph(wall_vertex, (0, 0))

    for ky in range(0, cell_top + 1):
        for kx in range(0, cell_width + 1):
            if (kx, ky) in graph:
                for x_cell in range(size * (ky - 1), size * ky):
                    for y_cell in range(size * (kx - 1), size * kx):
                        pixels[x_cell][y_cell] = np.array((0, 255, 0))

    (Image.fromarray(pixels, 'RGB').
     save('../tmp_photo/coloring_warehouse.png'))

    image = Image.open('../tmp_photo/coloring_warehouse.png')
    draw = ImageDraw.Draw(image)

    for x_cell in range(offset_x - size, width, size):
        if 0 <= x_cell < width:
            draw.line((x_cell, 0, x_cell, height),
                      fill=color_cell, width=width_line)

    for y_cell in range(offset_y - size, height, size):
        if 0 <= y_cell < height:
            draw.line((0, y_cell, width, y_cell),
                      fill=color_cell, width=width_line)

    image.save('../mesh_of_warehouse/warehouse_meshed.png')
    coloring_cell('../mesh_of_warehouse/warehouse_meshed.png',
                  operation_zone_x + left - size, operation_zone_y + top - size,
                  size, color=(0, 100, 100), width_line=width_line)

    # -3 - стена
    # -2 - внутреннее препятствие
    # -1 - стартовая зона
    #  0 - пустая ячейка

    matrix = np.array(
        [[-2 for _ in range(cell_width + 1)] for _ in range(cell_top + 1)])

    for i in bfs(wall_graph, (0, 0)):
        matrix[i[1]][i[0]] = -3

    ozy_cell = (operation_zone_y + top) // size
    ozx_cell = (operation_zone_x + left) // size
    for i in vertex:
        matrix[i[1]][i[0]] = 0
    matrix[ozy_cell][ozx_cell] = -1

    for i in matrix:
        for j in i:
            print(j, end=" ")
        print()

    mouse = np.array([ozx_cell, ozy_cell])



if __name__ == "__main__":
    mesh_function('../outline_of_warehouse/img.png',
                  250, 210, 30)
