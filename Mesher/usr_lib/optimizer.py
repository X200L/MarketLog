import heapq
import copy
import numpy as np

from Mesher.usr_lib.coloring_cell import coloring_cell
from Mesher.usr_lib.route_builder import route_builder
from Mesher.usr_lib.search_bfs import search_bfs
from Mesher.usr_lib.create_graph import create_graph
from Mesher.usr_lib.matrix_to_json import matrix_to_json
from Mesher.usr_lib.score_function import score_function
from Mesher.usr_lib.dist_on_road import dist_on_road
from Mesher.usr_lib.get_await_zone import get_await_zone


def optimizer(matrix, graphic_data, road_step=(None, None), charging_flag=True,
              charging=0, road_weight=1, pallet_weight=1,
              await_zone_size=(2, 2), priority_vec_az=('h', 'v')):
    size, width_line = graphic_data

    vertex = []
    operation_zones = []

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == -1:
                operation_zones.append((j + 1, i + 1))

            if matrix[i][j] not in {-3, -2}:
                vertex.append((j + 1, i + 1))

    graph = create_graph(vertex, operation_zones[0])
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
                      width_line=width_line, color=(100, 100, 100))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[0] * size, c[1] * size), pallets), size,
                      width_line=width_line, color=(255, 255, 0))

        matrix = copy.deepcopy(matrix_const)

        roads_list = [[]]

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
            if road_step[0] is not None:
                my_range = [roads_list[1][-1]]
                for s in range(0, len(roads_list[1]), road_step[0] + 1):
                    my_range.append(roads_list[1][s])

            else:
                my_range = [roads_list[1][0], roads_list[1][-1]]

            finish = roads_list[0]

            for e in [route_builder(graph, start, finish) for start
                      in my_range]:
                for i in e:
                    if matrix[i[1] - 1][i[0] - 1] not in {-3, -2}:
                        new_road.add(i)

            roads_list[0].extend(roads_list.pop(1))

        for i in operation_zones:
            for j in route_builder(graph, i, roads_list[0]):
                if matrix[j[1] - 1][j[0] - 1] in {0, 1}:
                    matrix[j[1] - 1][j[0] - 1] = 4
                    new_road.add(j)

        for i in new_road:
            matrix[i[1] - 1][i[0] - 1] = 4

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_road), size, width_line=width_line,
                      color=(100, 100, 100))

        for i in operation_zones:
            matrix[i[1] - 1][i[0] - 1] = -1

        await_zone = []
        for i in operation_zones:
            flag = False
            for t in search_bfs(graph, i):
                x, y = await_zone_size
                for var in get_await_zone(t[1] - 1, t[0] - 1, x, y,
                                          priority=priority_vec_az[0]):
                    try:
                        if all([matrix[c[1], c[0]] not in {-3, -2, -1, 2} for c
                                in
                                var]):
                            flag = True
                            await_zone.append(var)
                            for k in var:
                                matrix[k[1]][k[0]] = 2

                            break
                    except IndexError:
                        continue
                if flag:
                    break

            if not flag:
                await_zone.append([])
                print(
                    f"Не удаётся разместить зону ожидания {i}, вариант: {way}")

        new_pallets = set()

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    if (matrix[i - 1][j] in {4, -1, 2} or matrix[i + 1][j]
                            in {4, -1, 2}
                            or matrix[i][j - 1] in {4, -1, 2}
                            or matrix[i][j + 1] in {4, -1, 2}):
                        new_pallets.add((j + 1, i + 1))
                        matrix[i][j] = 1

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_pallets), size, width_line=width_line,
                      color=(255, 255, 0))

        new_road = set()

        for i in zip(operation_zones, await_zone):
            for j in route_builder(graph, i[0], i[1]):
                if matrix[j[1] - 1][j[0] - 1] not in {-3, -2, -1, 2}:
                    matrix[j[1] - 1][j[0] - 1] = 4
                    new_road.add(j)

        for i in new_road:
            matrix[i[1] - 1][i[0] - 1] = 4

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_road), size, width_line=width_line,
                      color=(100, 100, 100))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      [(i[0] * size - size,
                        i[1] * size - size) for i in operation_zones],
                      size, color=(0, 100, 100),
                      width_line=width_line)

        awz = []
        for i in await_zone:
            for j in i:
                awz.append(j)

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0]) * size, (c[1]) * size),
                          awz), size, width_line=width_line,
                      color=(0, 255, 255))

        dst = dist_on_road(matrix, operation_zones)

        ch_now = 0
        ch = []
        ch_nb = []
        fp = set()

        if charging_flag:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if ch_now < charging:
                        if matrix[i][j] == 0:
                            ch_nb.clear()

                            if matrix[i + 1][j] == 1:
                                ch_nb.append((i + 1, j))

                            if matrix[i - 1][j] == 1:
                                ch_nb.append((i - 1, j))

                            if matrix[i][j + 1] == 1:
                                ch_nb.append((i, j + 1))

                            if matrix[i][j - 1] == 1:
                                ch_nb.append((i, j - 1))

                            try:
                                fp.add(min(ch_nb, key=lambda c: dst[c]))
                                matrix[i][j] = 3
                                ch.append((j, i))
                                ch_now += 1
                            except ValueError:
                                continue
        q = []
        heapq.heapify(q)
        for i in dst:
            heapq.heappush(q, (-1 * dst[i], i))
        while ch_now < charging and len(q) > 0:
            tmp = heapq.heappop(q)[1]

            if matrix[tmp[0]][tmp[1]] == 1:
                if (tmp[0], tmp[1]) not in fp:
                    ch_now += 1
                    ch.append((tmp[1], tmp[0]))
                    matrix[tmp[0]][tmp[1]] = 3

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0]) * size, (c[1]) * size),
                          ch), size,
                      width_line=width_line,
                      color=(0, 255, 0))

        walls = set()
        empty = set()
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    empty.add((i, j))

                if matrix[i][j] in {-3, -2}:
                    walls.add((i, j))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[1] * size, c[0] * size),
                          empty), size, width_line=width_line,
                      color=(255, 255, 255))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[1] * size, c[0] * size),
                          walls), size, width_line=width_line,
                      color=(255, 0, 0))

        matrix_to_json(matrix, f'../graph/graph{way}.json')
        pal, mid_len, charg = score_function(matrix, operation_zones,
                                             f'../heatmaps/heatmap{way}.png')
        print(
            f"Вариант №{way}: {pal} - стеллажей, {mid_len} - среднее растояние до стеллажа, {charg} - зарядок")

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
                      width_line=width_line, color=(100, 100, 100))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[0] * size, c[1] * size), pallets), size,
                      width_line=width_line, color=(255, 255, 0))

        matrix = copy.deepcopy(matrix_const)

        roads_list = [[]]

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
        roads_list = list(filter(lambda c: c != [], roads_list))

        for i in range(len(roads_list)):
            for j in range(len(roads_list[i])):
                roads_list[i][j] = (roads_list[i][j][1] +
                                    1, roads_list[i][j][0] + 1)

        new_road = set()
        while len(roads_list) > 1:
            if road_step[-1] is not None:
                my_range = [roads_list[1][-1]]
                for s in range(0, len(roads_list[1]), road_step[-1] + 1):
                    my_range.append(roads_list[1][s])

            else:
                my_range = [roads_list[1][0], roads_list[1][-1]]

            finish = roads_list[0]

            for e in [route_builder(graph, start, finish) for start
                      in my_range]:
                for i in e:
                    if matrix[i[1] - 1][i[0] - 1] not in {-3, -2}:
                        new_road.add(i)

            roads_list[0].extend(roads_list.pop(1))

        for i in operation_zones:
            for j in route_builder(graph, i, roads_list[0]):
                if matrix[j[1] - 1][j[0] - 1] in {0, 1}:
                    matrix[j[1] - 1][j[0] - 1] = 4
                    new_road.add(j)

        for i in new_road:
            matrix[i[1] - 1][i[0] - 1] = 4

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_road), size, width_line=width_line,
                      color=(100, 100, 100))

        for i in operation_zones:
            matrix[i[1] - 1][i[0] - 1] = -1

        await_zone = []
        for i in operation_zones:
            flag = False
            for t in search_bfs(graph, i):
                x, y = await_zone_size
                for var in get_await_zone(t[1] - 1, t[0] - 1, x, y,
                                          priority=priority_vec_az[-1]):
                    try:
                        if all([matrix[c[1], c[0]] not in {-3, -2, -1, 2} for c
                                in
                                var]):
                            flag = True
                            await_zone.append(var)
                            for k in var:
                                matrix[k[1]][k[0]] = 2

                            break
                    except IndexError:
                        continue
                if flag:
                    break

            if not flag:
                await_zone.append([])
                print(
                    f"Не удаётся разместить зону ожидания {i}, вариант: {way}")

        new_pallets = set()

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    if (matrix[i - 1][j] in {4, -1, 2} or matrix[i + 1][j]
                            in {4, -1, 2}
                            or matrix[i][j - 1] in {4, -1, 2}
                            or matrix[i][j + 1] in {4, -1, 2}):
                        new_pallets.add((j + 1, i + 1))
                        matrix[i][j] = 1

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_pallets), size, width_line=width_line,
                      color=(255, 255, 0))

        new_road = set()

        for i in zip(operation_zones, await_zone):
            for j in route_builder(graph, i[0], i[1]):
                if matrix[j[1] - 1][j[0] - 1] not in {-3, -2, -1, 2}:
                    matrix[j[1] - 1][j[0] - 1] = 4
                    new_road.add(j)
        for i in new_road:
            matrix[i[1] - 1][i[0] - 1] = 4

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0] - 1) * size, (c[1] - 1) * size),
                          new_road), size, width_line=width_line,
                      color=(100, 100, 100))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      [(i[0] * size - size,
                        i[1] * size - size) for i in operation_zones],
                      size, color=(0, 100, 100),
                      width_line=width_line)

        awz = []
        for i in await_zone:
            for j in i:
                awz.append(j)

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0]) * size, (c[1]) * size),
                          awz), size, width_line=width_line,
                      color=(0, 255, 255))

        dst = dist_on_road(matrix, operation_zones)

        ch_now = 0
        ch = []
        ch_nb = []
        fp = set()

        if charging_flag:
            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    if ch_now < charging:
                        if matrix[i][j] == 0:
                            ch_nb.clear()

                            if matrix[i + 1][j] == 1:
                                ch_nb.append((i + 1, j))

                            if matrix[i - 1][j] == 1:
                                ch_nb.append((i - 1, j))

                            if matrix[i][j + 1] == 1:
                                ch_nb.append((i, j + 1))

                            if matrix[i][j - 1] == 1:
                                ch_nb.append((i, j - 1))

                            try:
                                fp.add(min(ch_nb, key=lambda c: dst[c]))
                                matrix[i][j] = 3
                                ch.append((j, i))
                                ch_now += 1
                            except ValueError:
                                continue
        q = []
        heapq.heapify(q)
        for i in dst:
            heapq.heappush(q, (-1 * dst[i], i))
        while ch_now < charging and len(q) > 0:
            tmp = heapq.heappop(q)[1]

            if matrix[tmp[0]][tmp[1]] == 1:
                if (tmp[0], tmp[1]) not in fp:
                    ch_now += 1
                    ch.append((tmp[1], tmp[0]))
                    matrix[tmp[0]][tmp[1]] = 3

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: ((c[0]) * size, (c[1]) * size),
                          ch), size,
                      width_line=width_line,
                      color=(0, 255, 0))

        walls = set()
        empty = set()
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    empty.add((i, j))

                if matrix[i][j] in {-3, -2}:
                    walls.add((i, j))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[1] * size, c[0] * size),
                          empty), size, width_line=width_line,
                      color=(255, 255, 255))

        coloring_cell(f'../tmp_photo/warehouse_roads{way}.png',
                      map(lambda c: (c[1] * size, c[0] * size),
                          walls), size, width_line=width_line,
                      color=(255, 0, 0))

        matrix_to_json(matrix, f'../graph/graph{way}.json')
        pal, mid_len, charg = score_function(matrix, operation_zones,
                                             f'../heatmaps/heatmap{way}.png')
        print(
            f"Вариант №{way}: {pal} - стеллажей, {mid_len} - среднее растояние до стеллажа, {charg} - зарядок")


if __name__ == "__main__":
    pass
