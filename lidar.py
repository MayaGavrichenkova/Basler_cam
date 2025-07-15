from rplidar import RPLidar
import sys
import numpy as np
PORT_NAME = '/dev/ttyUSB0' #имя порта для подключения
def run(path):
    lidar = RPLidar(PORT_NAME)#инициализация через порт
    data = []
    try:
        print('stop cntrl c')
        for scan in lidar.iter_scans():#скан из генератора скандо тип качество угол расстояние 
            data.append(np.array(scan))
    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
    np.save(path, np.array(data))

if __name__ == '__main__':
    run(sys.argv[1])#строка при запуске скрипта