import serial
import time

py_serial = serial.Serial(
    port = 'COM5',
    baudrate=9600,
)

while True:
    commend = input('hello')
    py_serial.write(commend.encode())
    
    time.sleep(0.1)
    
    if py_serial.readable():
        response = py_serial.readline()
        print(response[:len(response)-1].decode())

# 테스트 결과 b'test'