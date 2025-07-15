from Mesher.usr_lib.search_bfs import search_bfs


def score_function(matrix, operation_zone):
    counter = 0
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

    dst = search_bfs(road_graph, (operation_zone[1] - 1, operation_zone[0] - 1), flag=True)
    all_len = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                counter += 1
                tmp = []
                for c in nb:
                    dy, dx = c
                    if matrix[i + dy][j + dx] in {-1, 0, 2, 4}:
                        tmp.append(dst[(i + dy, j + dx)])

                all_len += min(tmp)

    return counter, all_len / counter
