import json

from Mesher.usr_lib.mesh_function import mesh_function


def starter(image_path, operation_zone_x, operation_zone_y, robot_size):
    mesh_function(image_path, operation_zone_x, operation_zone_y, robot_size)


if __name__ == "__main__":
    starter('../outline_of_warehouse/img2.png',
            300, 250, 5)

