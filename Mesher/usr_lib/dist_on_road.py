from Mesher.usr_lib.search_bfs import search_bfs


def dist_on_road(matrix, start):
    road_graph = {}
    nb = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] in {-1, 0, 2, 4}:
                tmp = []
                for c in nb:
                    dy, dx = c
                    if matrix[i + dy][j + dx] in {-1, 0, 2, 4}:
                        tmp.append((i + dy, j + dx))
                road_graph[(i, j)] = tmp

    best_tmp = {}
    for i in start:
        r = search_bfs(road_graph, (i[1] - 1, i[0] - 1), flag=True)
        for j in r:
            if j in best_tmp:
                best_tmp[j] = min(best_tmp[j], r[j])
            else:
                best_tmp[j] = r[j]

    res = {}
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                tmp = []
                for c in nb:
                    dy, dx = c
                    if matrix[i + dy][j + dx] in {-1, 0, 2, 4}:
                        tmp.append(best_tmp[(i + dy, j + dx)] + 1)

                res[(i, j)] = min(tmp) + 1

    return res
