# 우노로 실행
# https://boa9448.tistory.com/8

import time

import serial

arduino = serial.Serial(port = "COM9", baudrate = 9600)

time.sleep(3)

arduino.write(b"holy shit")

time.sleep(8)

data = arduino.read_all()

print(data)

arduino.close()

# 테스트 결과 b'test'