'''
@Author  ：skywoodsz
@Date    ：2025/6/4 11:17 
'''

from urdfpy import URDF
import os

if __name__ == '__main__':
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    urdf_path = os.path.join(parent_dir, "urdf", "sirius_diff.urdf")
    print(urdf_path)
    robot = URDF.load(urdf_path)
    for link in robot.links:
        print(link.name)

    robot.show()