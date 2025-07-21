import sys

from Mesher.usr_lib.mesh_function import mesh_function
from Mesher.usr_lib.prepare_matrix import prepare_matrix
from Mesher.usr_lib.optimizer import optimizer


def starter(input_data, operation_zones=None, robot_size=None,
            mode='p', charging=0, charging_flag=True, await_zone_size=(2, 2),
            priority_vec_az=('h', 'v'), road_step=(None, None)):
    if mode == 'p':
        if operation_zones is None or robot_size is None:
            print("Не указаны координаты операционных зон или размер робота!")
            sys.exit()

        const_matrix, *graphic_data = mesh_function(input_data,
                                                    operation_zones,
                                                    robot_size)

        optimizer(const_matrix, graphic_data, charging=charging,
                  charging_flag=charging_flag, await_zone_size=await_zone_size,
                  priority_vec_az=priority_vec_az, road_step=road_step)

    elif mode == 'm':
        const_matrix, *graphic_data = prepare_matrix(input_data)

        optimizer(const_matrix, graphic_data, charging=charging,
                  charging_flag=charging_flag, await_zone_size=await_zone_size,
                  priority_vec_az=priority_vec_az, road_step=road_step)


if __name__ == "__main__":
    try:
        starter('../outline_of_warehouse/img4.png',
                [(580 - 270 - 210, 200 - 30 + 210),
                 (580 - 240 - 180 - 60, 200 - 30 + 120),
                 (580 - 150 - 180 - 150, 200 + 180 + 120 + 30)]
                , 30,
                charging=15, await_zone_size=(2, 4),
                charging_flag=True, road_step=(13, 7))

    except Exception as error:
        print(f"Ошибка выполенния кода: {error}")
        sys.exit()
