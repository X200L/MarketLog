import numpy as np
import heapq


def dijkstra_for_matrix(matrix, start, targets_set, road_weight=0, pallet_weight=1):
    sx, sy = start
    rows = len(matrix)
    cols = len(matrix[0])
    neighbour = ((-1, 0), (1, 0), (0, -1), (0, 1))

    dist = np.array([[float('inf') for _ in range(cols)] for _ in range(rows)])
    prev = np.array([[None for _ in range(cols)] for _ in range(rows)])

    dist[sy][sx] = 0

    heap = []
    heapq.heappush(heap, (0, 0, (sx, sy)))
    counter = 1

    while heap:
        current_dist, _, cx, cy = heapq.heappop(heap)

        if (cy, cx) in targets_set:
            break

        if current_dist > dist[sy][sx]:
            continue










if __name__ == "__main__":