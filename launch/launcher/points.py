import yaml

def newPoint(data = None):
    if data:
        #x = float(data.split('x')[1].split('y')[0])
        #y = float(data.split('y')[1].split('n')[0])
        #name = data.split('n')[1]

        with open(f'src/krendel2/launch/launcher/points.txt', 'a') as f:
            f.write('\n' + data)

def deletePoint(data=None):
    if data:
        #x = float(data.split('x')[1].split('y')[0])
        #y = float(data.split('y')[1].split('n')[0])
        name = data.split(':')[1]

        oldData = readPoints()
        del oldData[name]
        newData = points2str(oldData)
        print(f"deleting {name}")

        with open(f'src/krendel2/launch/launcher/points.txt', 'w') as f:
            f.write(newData + "\n")

def readPoints() -> dict:
    data = ""
    with open(f'src/krendel2/launch/launcher/points.txt', 'r') as f:
        data= f.read()
    result = {}
    if data:
        data = data.split('\n')

        for pointData in data:
            if pointData:
                x = float(pointData.split('x')[1].split('y')[0])
                y = float(pointData.split('y')[1].split('n')[0])
                name = pointData.split('n')[1]

                result[name] = (x, y)

    return result

def points2str(points:dict) -> str:
    result = []
    if points:
        for point in points.items():
            result.append(f"p:x{point[1][0]}y{point[1][1]}n{point[0]}")

    result = "\n".join(result)
    
    return result