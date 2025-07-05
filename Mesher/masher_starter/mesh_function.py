import numpy as np

from PIL import ImageDraw, Image
from Mesher.usr_lib.add_borders import add_borders
from Mesher.usr_lib.create_graph import create_graph
from Mesher.usr_lib.coloring_cell import coloring_cell

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

    add_borders(image_path, 'Mesher/tmp_photo/bordered_image.png',
                left, right, top, bottom)

    pixels = np.array(Image.open('Mesher/tmp_photo/bordered_image.png'))

    height += top + bottom
    width += left + right
    offset_x += left
    offset_y += top

    cell_top = height // size
    cell_width = width // size

    vertex = []

    for ky in range(1, cell_top + 1):
        for kx in range(1, cell_width + 1):
            cell_middle_color = np.array([0, 0])
            for x_cell in range(size * (ky - 1), size * ky):
                for y_cell in range(size * (kx - 1), size * kx):
                    if pixels[x_cell][y_cell][0] > pixels[x_cell][y_cell][2]:
                        cell_middle_color[0] += 1
                    else:
                        cell_middle_color[1] += 1

            if cell_middle_color[1] / (cell_middle_color[0] +
                                       cell_middle_color[1]) >= 1 - epsilon:
                color = (0, 255, 0)
                vertex.append((kx - 1, ky - 1))

            else:
                color = (255, 0, 0)

            for x_cell in range(size * (ky - 1), size * ky):
                for y_cell in range(size * (kx - 1), size * kx):
                    pixels[x_cell][y_cell] = np.array(color)

    (Image.fromarray(pixels, 'RGB').
     save('Mesher/tmp_photo/coloring_warehouse.png'))

    img_tmp = Image.open('Mesher/tmp_photo/coloring_warehouse.png')
    draw = ImageDraw.Draw(img_tmp)

    for x_cell in range(offset_x - size, width, size):
        if 0 <= x_cell < width:
            draw.line((x_cell, 0, x_cell, height),
                      fill=color_cell, width=width_line)

    for y_cell in range(offset_y - size, height, size):
        if 0 <= y_cell < height:
            draw.line((0, y_cell, width, y_cell),
                      fill=color_cell, width=width_line)

    img_tmp.save('Mesher/mesh_of_warehouse/warehouse_meshed.png')

    coloring_cell('Mesher/mesh_of_warehouse/warehouse_meshed.png',
                  operation_zone_x + left, operation_zone_y + top,
                  size, color=(0, 100, 100), width_line=width_line)

    return create_graph(vertex, ((operation_zone_x + left) // size,
                                 (operation_zone_y + top) // size))


if __name__ == "__main__":
    mesh_function('Mesher/outline_of_warehouse/image.jpeg',
                  500, 450, 10)
