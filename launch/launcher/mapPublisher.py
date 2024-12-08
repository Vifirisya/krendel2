from flask import Flask, render_template, Response, request, redirect
import os
from PIL import Image
import yaml
import points
from zipfile import ZipFile
import time

ip = ""
with open(os.path.realpath(__file__).replace(f"/mapPublisher.py", "") + "/ip.txt", "r") as f:
    ip = f.read()

app = Flask(__name__, static_folder= os.path.realpath(__file__).replace(f"/mapPublisher.py", ""))
fileName = 'map'
scriptsFolder = 'scripts'

png = "launcher/map.png" #os.path.realpath(__file__).replace(f"/mapPublisher.py", "") + f"/{fileName}.png"
  
def get_all_file_paths(directory): 
    file_paths = [] 
  
    for root, directories, files in os.walk(directory): 
        for filename in files: 
            filepath = os.path.join(root, filename) 
            file_paths.append(filepath) 
  
    return file_paths   

@app.route('/map')
def mapImage():
    global fileName
    global png

    try:
        os.system(f'ros2 run nav2_map_server map_saver_cli -f src/krendel2/launch/launcher/{fileName}')

        #time.sleep(3)

        new_file = f"src/krendel2/launch/launcher/{fileName}.png"
        with Image.open(f"src/krendel2/launch/launcher/{fileName}.pgm") as im:
            im.save(new_file)
    except FileNotFoundError:
        pass
    finally:
        pass

    #return render_template('img.html', pngImg=png)
    return redirect('http://192.168.50.217:2003/launcher/map.png', code=302)

@app.route('/data')
def mapData():
    mapParams = ''

    with open(f'src/krendel2/launch/launcher/{fileName}.yaml') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            mapParams += 'r' + str(data['resolution'])
            mapParams += 'o' + str(data['origin'][0]) + ',' + str(data['origin'][1]) + ',' + str(data['origin'][2])

    return render_template('text.html', text=mapParams)

@app.route('/points')
def mapPoints():
    pointsData = points.points2str(points.readPoints())
    if pointsData == "":
        pointsData = "no points"
    
    return render_template('text.html', text=pointsData)

@app.route('/scripts', methods=['POST', 'GET'])
def code():
    if request.method == 'POST':
        data = request.data.decode('UTF-8')

        with open('src/krendel2/launch/launcher/scripts/main.py', 'w') as f:
            f.write(data)

    '''file_paths = get_all_file_paths(directory) 
  
    # printing the list of all files to be zipped 
    print('Following files will be zipped:') 
    for file_name in file_paths: 
        print(file_name) 
  
    # writing files to a zipfile 
    with ZipFile('my_python_files.zip','w') as zip: 
        # writing each file one by one 
        for file in file_paths: 
            zip.write(file) '''
    
    return 'code transfer'

if __name__ == '__main__':
    app.run(debug=True, host=ip, port=2003)