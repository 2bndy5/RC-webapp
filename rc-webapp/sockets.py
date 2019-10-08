from flask_socketio import SocketIO, emit
from circuitpython_mpu6050 import MPU6050
from adafruit_lsm9ds1 import LSM9DS1_I2C

from .hardware_io.check_platform import ON_RASPI, ON_WINDOWS  # , ON_JETSON
from .hardware_io.config import d_train, IMUs, gps, nav
from .hardware_io.imu import MAG3110, calc_heading, calc_yaw_pitch_roll
from .hardware_io.camera_manager import CameraManager

socketio = SocketIO(logger=False, engineio_logger=False, async_mode='eventlet')

def getHYPR():
    heading = []
    yaw = 0
    pitch = 0
    roll = 0
    for imu in IMUs:
        if type(imu, LSM9DS1_I2C):
            heading.append(calc_heading(imu.magnetic))
            yaw, pitch, roll = calc_yaw_pitch_roll(imu.acceleration, imu.gyro)
        elif type(imu, MAG3110):
            heading.append(imu.get_heading())
    if not heading:
        heading.append(0)
    print('heading:', heading[0], 'yaw:', yaw, 'pitch:', pitch, 'roll:', roll)
    return [heading[0], yaw, pitch, roll]


def get_imu_data():
    '''
    senses[0] = accel[x,y,z]
    senses[1] = gyro[x,y,z]
    senses[2] = mag[x,y,z]
    '''
    senses = [
        [100, 50, 25],
        [-100, -50, -25],
        [100, -50, 25]
    ]

    for imu in IMUs:
        if isinstance(imu, LSM9DS1_I2C):
            senses[0] = list(imu.acceleration)
            senses[1] = list(imu.gyro)
            senses[2] = list(imu.magnetic)
        elif isinstance(imu, MPU6050):
            senses[0] = list(imu.acceleration)
            senses[1] = list(imu.gryo)
    return senses

@socketio.on('connect')
def handle_connect():
    print('websocket Client connected!')

@socketio.on('disconnect')
def handle_disconnect():
    print('websocket Client disconnected')

@socketio.on('remoteOut')
def handle_remoteOut(arg):
    # for debugging
    print('remote =', repr(arg))
    if d_train: # if there is a drivetrain connected
        d_train[0].go([arg[0] * 655.35, arg[1] * 655.35])
