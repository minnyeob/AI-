import cv2
# mp = 미디어파이프에서 가져옴
import mediapipe as mp
# np = numpy에서 가져옴
import numpy as np
mp_drawing = mp.solutions.drawing_utils
# 미디어파이프의 Pose 기능
mp_pose = mp.solutions.pose

    
    
    
# 카운터에 사용할 변수 지정
# 횟수
left_counter = 0 
right_counter = 0 

# 팔의 상황
left_stage = None
right_stage = None

# 완료상태
left_done = None
right_done = None

#set 수
work_set = 0 

#비디오 확인
video_check = 0


# 새로 함수를 생산
def calculate_angle_left(a,b,c):
    # 배열 형태
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    # 각도계산
    #                     Y값          X값
    # 아크탄젠트로 C(끝)과 B(중간)의 각도를 구함  - A와 B의 각도를 구함
    # arctan2는 각도를 360도(0~180,0~-180)로 구할 수 있음
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    #                             원주율
    left_angle = np.abs(radians*180.0/np.pi)
    
    # 팔이 꺾여서 인식이 잘못되는 걸 방지
    if left_angle >180.0:
        left_angle = 360-left_angle
        
    return left_angle 

def calculate_angle_right(a,b,c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    right_angle = np.abs(radians*180.0/np.pi)
    
    if right_angle >180.0:
        right_angle = 360-right_angle
        
    return right_angle 









# 카메라 연결
cap = cv2.VideoCapture(0)

# 카메라가 연결되어있는동안
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        
        
        # ret = 반환 , farame = 영상
        ret, frame = cap.read()
        
        # 영상을 BRG에서 RGB로 변환
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # 포즈 프레임 불러오기
        results = pose.process(image)
    
        # 영상을 RGB에서 BRG로 전환
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 시도해보고 오류나면 except실행
        try:
            video_check = 1
            cv2.putText(image, 'success', (10,450), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,255,255),1,cv2.LINE_AA)
            
            landmarks = results.pose_landmarks.landmark
            
            #각 shoulder, elbow, writst에 랜드마크 값을 삽입
            #이때 shoulder, elobw, wirtst 대신 어깨, 엉덩이, 무릎으로 지정시 스쿼트 자세 교정 프로그램 가능
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
           
           
           
           
            # 각도계산
            left_angle = calculate_angle_left(left_shoulder, left_elbow, left_wrist)
            right_angle = calculate_angle_left(right_shoulder, right_elbow, right_wrist)
            
            
            
            
            # 각도 시각화
            cv2.putText(image, str(left_angle), 
                           tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            cv2.putText(image, str(right_angle), 
                           tuple(np.multiply(right_elbow, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
            
            
            
            # 암컬 카운터 알고리즘
            # 각도가 160도 이상이면 down으로 인식
            if left_angle > 155:
                left_stage = "left_down"
            if left_angle < 30 and left_stage =='left_down':
                left_stage="left_up"
                left_counter += 1
                
                print(left_counter)
                
                
                
                
            if right_angle > 155:
                right_stage = "right_down"
            if right_angle < 30 and right_stage =='right_down':
                right_stage="right_up"
                right_counter += 1
                
                print(right_counter)
            # 각도가 30도 이하고 상태가 down 이면 up으로 만들고 1증가
                
                
                
            if left_counter == 10 :
                left_counter = 0
                left_done = 1
            if right_counter == 10 :
                right_counter = 0
                right_done =1
                
            if left_done==1 & right_done==1:
                work_set +=1
                left_done = 0
                right_done = 0
                
                
            if work_set == 3:
                break
            
                
        except:
            if video_check == 0:
                cv2.putText(image, 'fail', (10,450), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255,255,255),1,cv2.LINE_AA)
        
            pass
        
        
    
        
        # 암컬 카운터 진행
        # 현재 상황 표시
        # 직사각형 생성 형태 시작점    종료점       색상      분수비트
        cv2.rectangle(image, (0,0),   (250,50),  (100,50,120),  -1)
        cv2.rectangle(image, (0,50),  (250,120), (245,117,16),  -1)
        cv2.rectangle(image, (0,120), (250,190), (245,100,100), -1)
        
        
        cv2.putText(image, 'set:', (0,45), cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255),2,cv2.LINE_AA)
        cv2.putText(image, str(work_set), (120,45), cv2.FONT_HERSHEY_DUPLEX, 2, (255,255,255),2,cv2.LINE_AA)
        
        # 횟수
        # 텍스트입력 형태    텍스트   좌표
        cv2.putText(image, 'left_REPS', (10,70), 
                    #     폰트지정            크기    색상   두께     선종류
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        #                   문자열 형태로 카운터 삽입
        cv2.putText(image, str(left_counter), 
                    (10,100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # up 인지 down인지
        
        # 좌측 횟수, 상태
        cv2.putText(image, 'left_STAGE', (100,70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, left_stage, 
                    (100,100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
        # 우측 횟수, 상태
        cv2.putText(image, 'right_REPS', (10,140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, str(right_counter), 
                    (10,170), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,50), 2, cv2.LINE_AA)
        
        cv2.putText(image, 'right_STAGE', (120,140), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
        cv2.putText(image, right_stage, 
                    (80,170), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,50), 2, cv2.LINE_AA)
        
        
        
        
        
        
        
        
        # 랜드마크 그리기, 색상설정
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()