import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from matplotlib.patches import Rectangle
from Mesher.usr_lib.dist_on_road import dist_on_road


def score_function(matrix, operation_zones, path=None):
    """Функция для получения метрик оценки топологии склада и
     составления heatmap"""

    counter = 0
    charg = 0
    score_matrix = np.array(
        [[float('inf') for _ in range(len(matrix[0]))] for _ in
         range(len(matrix))])

    dst = dist_on_road(matrix, operation_zones)
    all_len = 0

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            # считаем зарядки
            if matrix[i][j] == 3:
                charg += 1

            # считаем стеллажи и расстояние до них
            if matrix[i][j] == 1:
                counter += 1

                score_matrix[i][j] = dst[(i, j)] + 1

                all_len += dst[(i, j)] + 1

    # сстроим heatmap
    if path is not None:
        plt.figure()
        plt.title(f"Heatmap топологии склада", fontsize=14)

        try:
            ax = sns.heatmap(score_matrix, cmap="autumn_r", square=True,
                             xticklabels=False, yticklabels=False, vmin=0,
                             vmax=max(dst.values()) * 1.5)
        except ValueError:
            ax = sns.heatmap(score_matrix, cmap="autumn_r", square=True,
                             xticklabels=False, yticklabels=False, vmin=0,
                             vmax=0)

        # выделяем посторонние объекты
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

        # считаем метрики топологии
        try:
            plt.suptitle(f"{counter} - стеллажей; {round(all_len / counter, 3)} - среднее растояние до стеллажа; {charg} - зарядок", y=0.07, fontsize=8)
            return counter, all_len / counter, charg

        # обработка ошибки, если в топологии нет ни одного стеллажа
        except ZeroDivisionError:
            return 0, float('inf'), charg

        # сохраняем heatmap
        finally:
            plt.savefig(path, dpi=300)

    # если путь сохранения файла не указан
    else:
        try:
            return counter, all_len / counter, charg

        # обработка ошибки, если в топологии нет ни одного стеллажа
        except ZeroDivisionError:
            return 0, float('inf'), charg


if __name__ == "__main__":
    pass
