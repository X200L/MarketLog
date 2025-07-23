import heapq

from collections import defaultdict


def route_builder(matrix, start, targets_set, road_weight=1,
                  pallet_weight=1):
    """Функция для построения кратчайшего пути от заданной
     точки до лббого из элементов указанного множества"""

    start = (start[1] - 1, start[0] - 1)
    targets_set = set(map(lambda c: (c[1] - 1, c[0] - 1), targets_set))
    neighbour = ((-1, 0), (1, 0), (0, -1), (0, 1))

    # переводим матрицу в граф
    graph = defaultdict(dict)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] not in {-3, -2}:
                for n in neighbour:
                    dy, dx = n

                    if matrix[i + dy][j + dx] == 1:
                        graph[(i, j)][(i + dy, j + dx)] = pallet_weight
                    elif matrix[i + dy][j + dx] not in {-3, -2}:
                        graph[(i, j)][(i + dy, j + dx)] = road_weight

    # ищим кратчайший путь по алгоритму Дейкстры
    dist = {start: 0}
    prev = {start: None}

    q = []
    heapq.heapify(q)
    heapq.heappush(q, (0, start))

    while q:
        d, u = heapq.heappop(q)
        if d > dist[u]:
            continue

        if u in targets_set:
            path = []
            current = u

            # востанавливаем путь
            while current is not None:
                path.append(current)
                current = prev.get(current)

            path.reverse()
            return path

        # проверяем соседние вершины
        for v, w in graph[u].items():
            new_dist = d + w

            if v not in dist or new_dist < dist[v]:
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(q, (new_dist, v))

    # выводим сообщение о возможной ошибке
    print("Нет пути!")


if __name__ == "main":
    pass
