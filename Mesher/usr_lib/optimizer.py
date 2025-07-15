import copy
import numpy as np

from itertools import chain
from Mesher.usr_lib.coloring_cell import coloring_cell
from Mesher.usr_lib.route_builder import route_builder
from Mesher.usr_lib.search_bfs import search_bfs
from Mesher.usr_lib.create_graph import create_graph
from Mesher.usr_lib.matrix_to_json import matrix_to_json
from Mesher.usr_lib.score_function import score_function


def optimizer(matrix, graphic_data, road_step=None, charging=0, road_weight=1,
              pallet_weight=1):
    size, width_line = graphic_data

    vertex = []
    operation_zone = (0, 0)
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == -1:
                operation_zone = (j + 1, i + 1)

            if matrix[i][j] not in {-3, -2}:
                vertex.append((j + 1, i + 1))

    graph = create_graph(vertex, operation_zone)
    matrix_const = copy.deepcopy(matrix)

    for way in range(0, 3):
        s = 0
        roads = []
        pallets = []

        for i in range(way + 1, len(matrix_const) - 1, 3):
            for j in range(1, len(matrix_const[0]) - 1):
                if matrix_const[i][j] in {-1, 0}:
                    roads.append(np.array([j, i]))

                if (matrix_const[i + 1][j] == 0 and matrix_const[i][j]
                        in {0, -1}):
                    pallets.append(np.array([j, i + 1]))
                    s += 1

                if (matrix_const[i - 1][j] == 0 and matrix_const[i][j]
                        in {-1, 0}):
                    pallets.append(np.array([j, i - 1]))
                    s += 1

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[0] * size, c[1] * size), roads), size,
                      width_line=width_line, color=(120, 120, 120))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[0] * size, c[1] * size), pallets), size,
                      width_line=width_line, color=(255, 255, 0))

        matrix = copy.deepcopy(matrix_const)

        roads_list = [[]]

        if way >= 3:
            for j in range(way + 1, len(matrix[0]) - 1, 3):
                for i in range(1, len(matrix) - 1):
                    if matrix[i][j] in {0, -1}:
                        if matrix[i][j] == 0:
                            matrix[i][j] = 4

                        roads_list[-1].append((i, j))
                    else:
                        roads_list.append([])

                    if matrix[i][j + 1] == 0 and matrix[i][j] in {4, -1}:
                        matrix[i][j + 1] = 1
                    if matrix[i][j - 1] == 0 and matrix[i][j] in {4, -1}:
                        matrix[i][j - 1] = 1

        else:
            for i in range(way + 1, len(matrix) - 1, 3):
                for j in range(1, len(matrix[0]) - 1):
                    if matrix[i][j] in {0, -1}:
                        if matrix[i][j] == 0:
                            matrix[i][j] = 4

                        roads_list[-1].append((i, j))
                    else:
                        roads_list.append([])

                    if matrix[i + 1][j] == 0 and matrix[i][j] in {4, -1}:
                        matrix[i + 1][j] = 1
                    if matrix[i - 1][j] == 0 and matrix[i][j] in {4, -1}:
                        matrix[i - 1][j] = 1

        roads_list = list(filter(lambda c: c != [], roads_list))
        for i in range(len(roads_list)):
            for j in range(len(roads_list[i])):
                roads_list[i][j] = (roads_list[i][j][1] +
                                    1, roads_list[i][j][0] + 1)

        new_road = set()
        while len(roads_list) > 1:
            start1 = roads_list[1][-1]
            start2 = roads_list[1][0]
            finish = roads_list[0]

            for i in chain(route_builder(graph, start1, finish),
                           route_builder(graph, start2, finish)):
                new_road.add(i)
                matrix[i[1] - 1][i[0] - 1] = 4

            roads_list[0].extend(roads_list.pop(1))

        for i in route_builder(graph, operation_zone,
                               roads_list[0]):
            matrix[i[1] - 1][i[0] - 1] = 4
            new_road.add(i)

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_road), size, width_line=width_line,
                      color=(120, 120, 120))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      [(operation_zone[0] * size - size,
                        operation_zone[1] * size - size)],
                      size, color=(0, 100, 100),
                      width_line=width_line)

        new_pallets = set()

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    if (matrix[i - 1][j] in {4, -1} or matrix[i + 1][j]
                            in {4, -1}
                            or matrix[i][j - 1] in {4, -1}
                            or matrix[i][j + 1] in {4, -1}):
                        new_pallets.add((j + 1, i + 1))
                        matrix[i][j] = 1

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_pallets), size, width_line=width_line,
                      color=(255, 255, 0))

        mc1, mc2, mc3, mc4 = None, None, None, None
        turn_zone = [mc1, mc2, mc3, mc4]
        matrix[operation_zone[1] - 1][operation_zone[0] - 1] = -1

        for i in search_bfs(graph, operation_zone):
            mc1 = (i[1], i[0])
            mc2 = (mc1[0] + 1, mc1[1])
            mc3 = (mc1[0], mc1[1] - 1)
            mc4 = (mc1[0] + 1, mc1[1] - 1)
            turn_zone = [mc1, mc2, mc3, mc4]
            if all([matrix[i[0]][i[1]] not in {-3, -2, -1} for i in turn_zone]):
                for j in turn_zone:
                    matrix[j[0]][j[1]] = 2
                break

        if mc1 is not None:
            coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                          map(lambda c: ((c[1]) * size, (c[0]) * size),
                              turn_zone), size,
                          width_line=width_line,
                          color=(0, 255, 255))
        else:
            print(f"{way} - Нет места для зоны поворота")

        vertex2 = []

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] not in {-3, -2}:
                    vertex2.append((j + 1, i + 1))

        graph2 = create_graph(vertex2, operation_zone)

        ch_now = 0
        chk = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if ch_now < charging:
                    if matrix[i][j] == 0:
                        matrix[i][j] = 3
                        chk.append((j, i))
                        ch_now += 1

        dst = search_bfs(graph2, operation_zone)
        while ch_now < charging and len(dst) > 0:
            tmp = dst.pop()
            if matrix[tmp[1] - 1][tmp[0] - 1] == 1:
                ch_now += 1
                chk.append((tmp[0] - 1, tmp[1] - 1))
                matrix[tmp[1] - 1][tmp[0] - 1] = 3

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0]) * size, (c[1]) * size),
                          chk), size,
                      width_line=width_line,
                      color=(155, 25, 155))

        matrix_to_json(matrix, f'../graph/graph{way}.json')
        pal, mid_len = score_function(matrix)
        print(f"Вариант №{way}: {pal} - стеллажей, {mid_len} - среднее растояние до стеллажа\n")

    for way in range(3, 6):
        s = 0
        roads = []
        pallets = []

        for i in range(1, len(matrix_const) - 1):
            for j in range((way + 1) % 3, len(matrix_const[0]) - 1, 3):
                if matrix_const[i][j] == 0:
                    roads.append(np.array([j, i]))

                if (matrix_const[i][j + 1] == 0 and matrix_const[i][j]
                        in {0, -1}):
                    pallets.append(np.array([j + 1, i]))
                    s += 1

                if (matrix_const[i][j - 1] == 0 and matrix_const[i][j]
                        in {0, -1}):
                    pallets.append(np.array([j - 1, i]))
                    s += 1

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[0] * size, c[1] * size), roads), size,
                      width_line=width_line, color=(120, 120, 120))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[0] * size, c[1] * size), pallets), size,
                      width_line=width_line, color=(255, 255, 0))

        matrix = copy.deepcopy(matrix_const)
        roads_list = [[]]

        if way >= 3:
            for j in range((way + 1) % 3, len(matrix[0]) - 1, 3):
                for i in range(1, len(matrix) - 1):
                    if matrix[i][j] in {0, -1}:
                        if matrix[i][j] == 0:
                            matrix[i][j] = 4

                        roads_list[-1].append((i, j))
                    else:
                        roads_list.append([])

                    if matrix[i][j + 1] == 0 and matrix[i][j] in {4, -1}:
                        matrix[i][j + 1] = 1
                    if matrix[i][j - 1] == 0 and matrix[i][j] in {4, -1}:
                        matrix[i][j - 1] = 1

        else:
            for i in range(way + 1, len(matrix) - 1, 3):
                for j in range(1, len(matrix[0]) - 1):
                    if matrix[i][j] in {0, -1}:
                        if matrix[i][j] == 0:
                            matrix[i][j] = 4

                        roads_list[-1].append((i, j))
                    else:
                        roads_list.append([])

                    if matrix[i + 1][j] == 0 and matrix[i][j] in {4, -1}:
                        matrix[i + 1][j] = 1
                    if matrix[i - 1][j] == 0 and matrix[i][j] in {4, -1}:
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

            for i in chain(route_builder(graph, start1, finish),
                           route_builder(graph, start2, finish)):
                new_road.add(i)
                matrix[i[1] - 1][i[0] - 1] = 4

            roads_list[0].extend(roads_list.pop(1))

        for i in route_builder(graph, operation_zone,
                               roads_list[0]):
            matrix[i[1] - 1][i[0] - 1] = 4
            new_road.add(i)

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_road), size, width_line=width_line,
                      color=(120, 120, 120))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      [(operation_zone[0] * size - size,
                        operation_zone[1] * size - size)],
                      size, color=(0, 100, 100),
                      width_line=width_line)

        new_pallets = set()

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    if (matrix[i - 1][j] in {4, -1} or matrix[i + 1][j] in {4,
                                                                            -1}
                            or matrix[i][j - 1] in {4, -1}
                            or matrix[i][j + 1] in {4, -1}):
                        new_pallets.add((j + 1, i + 1))
                        matrix[i][j] = 1

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_pallets), size, width_line=width_line,
                      color=(255, 255, 0))

        mc1, mc2, mc3, mc4 = None, None, None, None
        turn_zone = [mc1, mc2, mc3, mc4]
        matrix[operation_zone[1] - 1][operation_zone[0] - 1] = -1

        for i in search_bfs(graph, operation_zone):
            mc1 = (i[1], i[0])
            mc2 = (mc1[0] + 1, mc1[1])
            mc3 = (mc1[0], mc1[1] - 1)
            mc4 = (mc1[0] + 1, mc1[1] - 1)
            turn_zone = [mc1, mc2, mc3, mc4]
            if all([matrix[i[0]][i[1]] not in {-3, -2, -1} for i in turn_zone]):
                for j in turn_zone:
                    matrix[j[0]][j[1]] = 2
                break

        if mc1 is not None:
            coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                          map(lambda c: ((c[1]) * size, (c[0]) * size),
                              turn_zone), size,
                          width_line=width_line,
                          color=(0, 255, 255))
        else:
            print(f"{way} - Нет места для зоны поворота")

        vertex2 = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] not in {-3, -2}:
                    vertex2.append((j + 1, i + 1))

        graph2 = create_graph(vertex2, operation_zone)

        ch_now = 0
        chk = []
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if ch_now < charging:
                    if matrix[i][j] == 0:
                        matrix[i][j] = 3
                        chk.append((j, i))
                        ch_now += 1

        dst = search_bfs(graph2, operation_zone)
        while ch_now < charging and len(dst) > 0:
            tmp = dst.pop()
            if matrix[tmp[1] - 1][tmp[0] - 1] == 1:
                ch_now += 1
                chk.append((tmp[0] - 1, tmp[1] - 1))
                matrix[tmp[1] - 1][tmp[0] - 1] = 3

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0]) * size, (c[1]) * size),
                          chk), size,
                      width_line=width_line,
                      color=(155, 25, 155))

        matrix_to_json(matrix, f'../graph/graph{way}.json')
        pal, mid_len = score_function(matrix)
        print(f"Вариант №{way}: {pal} - стеллажей, {mid_len} - среднее растояние до стеллажа\n")
