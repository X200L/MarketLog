from Mesher.usr_lib.mesh_function import mesh_function
from Mesher.usr_lib.optimizer import optimizer


def starter(input_data, operation_zone_x, operation_zone_y, robot_size,
            mode='p'):
    if mode == 'p':
        const_matrix, *graphic_data = mesh_function(input_data,
                                                    operation_zone_x,
                                                    operation_zone_y,
                                                    robot_size)

        optimizer(const_matrix, graphic_data, charging=5)

    elif mode == 'm':
        pass


if __name__ == "__main__":
    starter('../outline_of_warehouse/img4.png',
            350, 200, 30)
