# from mesh_function import mesh_function
from backend.optimizer import optimizer
from backend.mesh_function import mesh_function

def starter(input_data, operation_zone_x, operation_zone_y, robot_size, chat_id,
            mode='p', temp_upload_folder=None):
    if mode == 'p':
        #print(chat_id)
        const_matrix, *graphic_data = mesh_function(input_data,
                                                    operation_zone_x,
                                                    operation_zone_y,
                                                    0,
                                                    robot_size,
                                                    temp_upload_folder=temp_upload_folder)

        optimizer(const_matrix, graphic_data, charging=5, temp_upload_folder=temp_upload_folder)


    elif mode == 'm':
        pass


if __name__ == "__main__":
    starter('../outline_of_warehouse/img4.png',
            350, 150, 30)