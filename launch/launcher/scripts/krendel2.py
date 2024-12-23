import points
import os

def go(pointName):
    p = points.readPoints()
    pos = p[pointName]

    os.system(f"ros2 topic pub /goal_pose geometry_msgs/PoseStamped \"{{header: {{stamp: {{sec: 0}}, frame_id: \'map\'}}, pose: {{position: {{x: {pos[0]}, y: {pos[1]}, z: 0.0}}, orientation: {{w: 1.0}}}}}}\"")