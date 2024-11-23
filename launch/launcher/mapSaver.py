import os
from PIL import Image
import time

fileName = "map"

while True:
    try:
        os.system(f'ros2 run nav2_map_server map_saver_cli -f src/krendel2/launch/launcher/templates/{fileName}')

        time.sleep(3)

        new_file = f"src/krendel2/launch/launcher/templates/{fileName}.png"
        with Image.open(f"{fileName}.pgm") as im:
            im.save(new_file)
    except FileNotFoundError:
        pass
    finally:
        pass