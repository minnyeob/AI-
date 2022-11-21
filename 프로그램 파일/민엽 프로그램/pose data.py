import cv2
import mediapipe as mp
import numpy as mp
import time, os

pose = ['come','back','left_spin', 'right spin','stop', 'all stop']

# 전진,후진,좌회전,회전, 정지, 시동종료순 녹화시작

rec_size        = 30
rec_action_time = 30

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


IMAGE_FILES = []
BG_COLOR = (192, 192, 192) 
with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    image_height, image_width, _ = image.shape
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
      continue
    print(
        f'Nose coordinates: ('
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
        f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
    )

    annotated_image = image.copy()
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1
    bg_image = np.zeros(image.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR
    annotated_image = np.where(condition, annotated_image, bg_image)
   
    mp_drawing.draw_landmarks(
        annotated_image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', annotated_image)
   
    mp_drawing.plot_landmarks(
        results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)


# 비디오 캡쳐
cap = cv2.VideoCapture(0)

# 비디오 캡쳐후 저장파일 생성 코드 이름 : pose_data
rec_time = int(time.time())
os.makedirs('pose_data', exist = True)

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
    
  #  캡처 도중일때
  while cap.isOpened():
    # 이미지 표시 성공여부
    success, image = cap.read()
    # 이미지 불러오기
    ret, img = cap.read()
    
    # 이미지 플립
    img = cv2.flip(img, 1)
    
    # collecting ? pose 를 띄움
    cv2.putText(img, f'Collecting {pose.upper()} pose', org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
    cv2.imshow('img', img)
    
    # 문자표시 시간
    cv2.waitkey(2000)
    
    start_time = time.time()
    
    # 설정 시간동안 반복    
    while time.time() - start_time < rec_action_time:
        ret, img = cap.read()
        
        img = cv2.flip(img, 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        result = pose.process(img)
           
        # 실패시 Ignoring empty camera frame 표시
        if not success:
            print("Ignoring empty camera frame.")
        continue
  
    

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
    
    
cap.release()
