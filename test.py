import serial
import time

# 'COM3' 부분에 환경에 맞는 포트 입력
ser = serial.Serial('COM8', 9600)

while True:
    if ser.readable():
        val = input()

        if val == '0':
            val = val.encode('utf-8')
            ser.write(val)
            print("set 1")
            time.sleep(0.5)

        elif val == '1':
            val = val.encode('utf-8')
            ser.write(val)
            print("set 2")
            time.sleep(0.5)
            
        elif val == '2':
            val = val.encode('utf-8')
            ser.write(val)
            print("set 3")
            time.sleep(0.5)