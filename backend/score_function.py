import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.patches import Rectangle
from search_bfs import search_bfs

import matplotlib
matplotlib.use('Agg')


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

    all_len = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 1:
                counter += 1
                tmp = []
                v = []
                for c in nb:
                    dy, dx = c
                    if matrix[i + dy][j + dx] in {-1, 0, 2, 4}:
                        tmp.append(dst[(i + dy, j + dx)] + 1)
                        v.append((i, j))

                all_len += min(tmp)
                score_matrix[v[tmp.index(min(tmp)) - 1][0]][v[tmp.index(min(tmp)) - 1][1]] = min(tmp)

    if path is not None:
        fig, ax = plt.subplots()

        ax = sns.heatmap(score_matrix, cmap="autumn_r", square=True,
                         xticklabels=False, yticklabels=False, vmin=0,
                         vmax=max(filter(lambda t: t != float('inf'),
                                         dst.values())) * 1.5)

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == -1:
                    ax.add_patch(Rectangle((j, i), 1, 1,
                                           facecolor=(0 / 255, 100 / 255,
                                                      100 / 255)))

                if matrix[i][j] in {-3, -2}:
                    ax.add_patch(Rectangle((j, i), 1, 1,
                                           facecolor=(200 / 255, 200 / 255,
                                                      200 / 255)))

                if matrix[i][j] == 4:
                    ax.add_patch(Rectangle((j, i), 1, 1,
                                           facecolor=(100 / 255, 100 / 255,
                                                      100 / 255)))

                if matrix[i][j] == 3:
                    ax.add_patch(Rectangle((j, i), 1, 1,
                                           facecolor=(0 / 255, 255 / 255,
                                                      0 / 255)))

                if matrix[i][j] == 2:
                    ax.add_patch(Rectangle((j, i), 1, 1,
                                           facecolor=(0 / 255, 255 / 255,
                                                      255 / 255)))

                if matrix[i][j] == 0:
                    ax.add_patch(Rectangle((j, i), 1, 1,
                                           facecolor=(255 / 255, 255 / 255,
                                                      255 / 255)))

        fig.savefig(path, dpi=300)
        plt.close(fig)

    return counter, all_len / counter
