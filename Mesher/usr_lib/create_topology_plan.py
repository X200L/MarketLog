from PIL import Image
from Mesher.usr_lib.remove_border import remove_border


def create_topology_plan(background, foreground, alpha, output_path,
                         border_info):
    res = Image.blend(Image.open(background),
                      remove_border(foreground, border_info), alpha)

    res.save(output_path)


if __name__ == '__main__':
    way = 0
    create_topology_plan('../outline_of_warehouse/1234.png',
                         f'../tmp_photo/warehouse_roads{way}.png',
                         0.3,
                         f'../topology_plan/topology_plan{way}.png',
                         f'../tmp_photo/border_info.json')
