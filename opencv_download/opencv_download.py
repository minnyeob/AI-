#jupyter 다운
#PyPI 다운
#파이선 버전을 3.7.9이하로 다운(OPENCV가 3.7.9위에서는 미지원)

# cmd를 관리자 권한으로 시행

# curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# python get-pip.py

# pip install --upgrade pip

# pip install notebook

# pip intall numpy

# pip install matplotlib

# python idle 실행
# python 은 파이선 홈페이지에서 다운로드
# 카메라 연결

#새 터미널 창

#python -m venv cv_env

# f1을 누른 후 찾기

# bin => python

# ctrl + ~

# cv_env 확인 = 가상환경으로 들어옴

# 관리자 모드로 powershell 
# set-ExecutionPolicy RemoteSigned
# '예' 설정

# 휴지통 누른 후 ctrl + ~

#터미널에서 pip install opencv-python
#-업데이트시 python -m pip install --upgrade pip

#pip 안될대 
# pip install bs4
# pip install beautifulsoup4
# pip install django

#
#   공대선배
#   opencv python 코딩
#   카메라 연결 코드
#

import cv2

# opencv python 코딩 기본 틀
# 카메라 영상을 받아올 객체 선언 및 설정(영상 소스, 해상도 설정)
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #가로해상도
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #세로해상도

# 무한루프
while True:
    ret, frame = capture.read()     # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret가 참
    cv2.imshow("original", frame)   # frame(카메라 영상)을 original 이라는 창에 띄워줌 
    if cv2.waitKey(1) == ord('q'):  # 키보드의 q 를 누르면 무한루프가 멈춤
            break

capture.release()                   # 캡처 객체를 없애줌
cv2.destroyAllWindows()             # 모든 영상 창을 닫아줌