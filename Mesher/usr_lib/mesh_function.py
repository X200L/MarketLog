import numpy as np

from itertools import chain
from PIL import ImageDraw, Image
from Mesher.usr_lib.add_borders import add_borders
from Mesher.usr_lib.create_graph import create_graph
from Mesher.usr_lib.coloring_cell import coloring_cell
from Mesher.usr_lib.search_bfs import search_bfs
from Mesher.usr_lib.route_bfs import route_bfs


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
    offset_x += size
    offset_y += size

    add_borders(image_path, '../tmp_photo/bordered_image.png',
                left, right, top, bottom, size)

    pixels = np.array(Image.open('../tmp_photo/bordered_image.png'))

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
                  [(operation_zone_x + left - size, operation_zone_y + top
                    - size)], size, color=(0, 100, 100), width_line=width_line)

    # -3 - стена
    # -2 - внутреннее препятствие
    # -1 - стартовая зона
    #  0 - пустая ячейка/дорога
    #  1 - ячейка хранения
    #  2 - зона поворота
    #  3 - зарядка

    matrix = np.array(
        [[-2 for _ in range(cell_width)] for _ in range(cell_top)])

    for i in search_bfs(wall_graph, (0, 0)):
        matrix[i[1] - 1][i[0] - 1] = -3

    ozy_cell = (operation_zone_y + top) // size - 1
    ozx_cell = (operation_zone_x + left) // size - 1
    for i in graph:
        matrix[i[1] - 1][i[0] - 1] = 0
    matrix[ozy_cell][ozx_cell] = -1

    img_copy = Image.open('../mesh_of_warehouse/warehouse_meshed.png')
    for i in range(0, 6):
        img_copy.save(f'../tmp_photo/warehouse_roads{i}.png')
    img_copy.close()

    res = []

    for t in range(0, 3):
        s = 0
        roads = []
        pallets = []

        for i in range(t + 1, len(matrix) - 1, 3):
            for j in range(1, len(matrix[0]) - 1):
                if matrix[i][j] == 0:
                    roads.append(np.array([j, i]))

                if matrix[i + 1][j] == 0 and matrix[i][j] in {0, -1}:
                    pallets.append(np.array([j, i + 1]))
                    s += 1

                if matrix[i - 1][j] == 0 and matrix[i][j] in {0, -1}:
                    pallets.append(np.array([j, i - 1]))
                    s += 1

        coloring_cell(f'../tmp_photo/warehouse_roads{t}.png',
                      map(lambda c: (c[0] * size, c[1] * size), roads), size,
                      width_line=width_line, color=(120, 120, 120))

        coloring_cell(f'../tmp_photo/warehouse_roads{t}.png',
                      map(lambda c: (c[0] * size, c[1] * size), pallets), size,
                      width_line=width_line, color=(255, 255, 0))

        res.append(s)

    for t in range(0, 3):
        s = 0
        roads = []
        pallets = []

        for i in range(1, len(matrix) - 1):
            for j in range(t + 1, len(matrix[0]) - 1, 3):
                if matrix[i][j] == 0:
                    roads.append(np.array([j, i]))

                if matrix[i][j + 1] == 0 and matrix[i][j] in {0, -1}:
                    pallets.append(np.array([j + 1, i]))
                    s += 1

                if matrix[i][j - 1] == 0 and matrix[i][j] in {0, -1}:
                    pallets.append(np.array([j - 1, i]))
                    s += 1

        coloring_cell(f'../tmp_photo/warehouse_roads{t + 3}.png',
                      map(lambda c: (c[0] * size, c[1] * size), roads), size,
                      width_line=width_line, color=(120, 120, 120))

        coloring_cell(f'../tmp_photo/warehouse_roads{t + 3}.png',
                      map(lambda c: (c[0] * size, c[1] * size), pallets), size,
                      width_line=width_line, color=(255, 255, 0))

        res.append(s)

    t = res.index(max(res))
    print("Выбрана схема:", t, "\n\n\n\n")

    t = res.index(max(res))

    roads_list = [[]]

    if t >= 3:
        for j in range(t + 1, len(matrix[0]) - 1, 3):
            for i in range(1, len(matrix) - 1):
                if matrix[i][j] in {0, -1}:
                    roads_list[-1].append((i, j))
                else:
                    roads_list.append([])

                if matrix[i][j + 1] == 0 and matrix[i][j] in {0, -1}:
                    matrix[i][j + 1] = 1
                if matrix[i][j - 1] == 0 and matrix[i][j] in {0, -1}:
                    matrix[i][j - 1] = 1

    else:
        for i in range(t + 1, len(matrix) - 1, 3):
            for j in range(1, len(matrix[0]) - 1):
                if matrix[i][j] in {0, -1}:
                    roads_list[-1].append((i, j))
                else:
                    roads_list.append([])

                if matrix[i + 1][j] == 0 and matrix[i][j] in {0, -1}:
                    matrix[i + 1][j] = 1
                if matrix[i - 1][j] == 0 and matrix[i][j] in {0, -1}:
                    matrix[i - 1][j] = 1

    roads_list = list(filter(lambda c: c != [], roads_list))
    for i in range(len(roads_list)):
        for j in range(len(roads_list[i])):
            roads_list[i][j] = (roads_list[i][j][1] +
                                1, roads_list[i][j][0] + 1)

    new_road = set()

    while len(roads_list) > 1:
        start1 = roads_list[1][0]
        start2 = roads_list[1][-1]
        finish = roads_list[0]

        for i in chain(route_bfs(graph, start1, finish), route_bfs(graph, start2, finish)):
            new_road.add(i)
            matrix[i[1] - 1][i[0] - 1] = 0

            for j in {(1, 0), (-1, 0), (0, 1), (0, -1)}:
                if matrix[i[1] - 1 + j[1]][i[0] - 1 - j[0]] == 0:
                    matrix[i[1] - 1 + j[1]][i[0] - 1 - j[0]] = 1

        roads_list[0].extend(roads_list.pop(1))
        # roads_list.remove()

    coloring_cell(f'../tmp_photo/warehouse_roads{t}.png',
                  map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                      new_road), size, width_line=width_line,
                  color=(120, 120, 120))

    for i in matrix:
        print('[', end='')
        for j in i:
            print(j, end=", ")
        print(']')
    print("\n\n\n\n")


if __name__ == "__main__":
    mesh_function('../outline_of_warehouse/img4.png',
                  400, 300, 30)
