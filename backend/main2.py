from mesh_function import mesh_function
from optimizer import optimizer


def starter(input_data, operation_zone_x, operation_zone_y, robot_size,
            mode='p', temp_upload_folder=None, user_dir=None):
    if mode == 'p':
        const_matrix, *graphic_data = mesh_function(input_data,
                                                    operation_zone_x,
                                                    operation_zone_y,
                                                    robot_size,
                                                    temp_upload_folder=temp_upload_folder,
                                                    user_dir=user_dir)

        optimizer(const_matrix, graphic_data, charging=5, temp_upload_folder=temp_upload_folder, user_dir=user_dir)

    elif mode == 'm':
        pass


if __name__ == "__main__":
    starter('../outline_of_warehouse/img4.png',
            350, 150, 30)