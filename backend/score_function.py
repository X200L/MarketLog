import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from backend.search_bfs import search_bfs


def score_function(matrix, operation_zone, path=None):
    counter = 0
    road_graph = {}
    nb = ((1, 0), (-1, 0), (0, 1), (0, -1))
    score_matrix = np.array(
        [[float('inf') for _ in range(len(matrix[0]))] for _ in
         range(len(matrix))])

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] in {-1, 0, 2, 4}:
                tmp = []
                for c in nb:
                    dy, dx = c
                    if matrix[i + dy][j + dx] in {-1, 0, 2, 4}:
                        tmp.append((i + dy, j + dx))
                road_graph[(i, j)] = tmp

    dst = search_bfs(road_graph, (operation_zone[1] - 1,
                                  operation_zone[0] - 1), flag=True)

    for i in dst:
        x, y = i
        score_matrix[x - 1][y - 1] = dst[i]

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

    if path is not None:
        plt.figure(figsize=(10, 8))
        sns.heatmap(score_matrix, cmap="Blues", vmin=0,
                    vmax=max(filter(lambda t: t != float('inf'), dst.values())))

        plt.savefig(path, dpi=300)



    return counter, all_len / counter