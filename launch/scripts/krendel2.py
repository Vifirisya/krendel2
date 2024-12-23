import os
import sys

sys.path.insert(0, os.path.realpath(__file__).replace(f"scripts/krendel2.py", "launcher"))

import points

def go(pointName):
    print("!SCRIPT! doing \"GO\" !SCRIPT!")
    p = points.readPoints()
    pos = p[pointName]
    os.system(f"ros2 topic pub /goal_pose geometry_msgs/PoseStamped \"{{header: {{stamp: {{sec: 0}}, frame_id: \'map\'}}, pose: {{position: {{x: {pos[0]}, y: {pos[1]}, z: 0.0}}, orientation: {{w: 1.0}}}}}}\"")