import sys

from Mesher.usr_lib.mesh_function import mesh_function
from Mesher.usr_lib.prepare_matrix import prepare_matrix
from Mesher.usr_lib.optimizer import optimizer


def starter(input_data, operation_zones=None, robot_size=None,
            mode='p', charging=0, charging_flag=True, await_zone_size=(2, 2),
            priority_vec_az=('h', 'v'), road_step=(None, None), pallet_weight=1,
            road_weight=1, alpha=0.5):
    """Функция запуска системы создания топологии склада"""

    # если на вход подаётся фотография
    if mode == 'p':
        if operation_zones is None or robot_size is None:
            print("Не указаны координаты операционных зон или размер робота!")
            sys.exit()

        const_matrix, *graphic_data = mesh_function(input_data, operation_zones,
                                                    robot_size)

        optimizer(const_matrix, graphic_data, charging=charging,
                  charging_flag=charging_flag, await_zone_size=await_zone_size,
                  priority_vec_az=priority_vec_az, road_step=road_step,
                  pallet_weight=pallet_weight, road_weight=road_weight,
                  mode='p', input_path=input_data, alpha=alpha)

    # если на вход подаётся матрица
    elif mode == 'm':
        const_matrix, *graphic_data = prepare_matrix(input_data)

        optimizer(const_matrix, graphic_data, charging=charging,
                  charging_flag=charging_flag, await_zone_size=await_zone_size,
                  priority_vec_az=priority_vec_az, road_step=road_step,
                  pallet_weight=pallet_weight, road_weight=road_weight,
                  mode='m')


if __name__ == "__main__":
    starter('../outline_of_warehouse/1234.png',
            charging=0, await_zone_size=(2, 2),
            charging_flag=True, mode='p', robot_size=24,
            operation_zones=[(800, 870)])
