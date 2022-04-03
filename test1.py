import mediapipe
import cv2
import math
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
# setup the GPIO pin for the servo
servo_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin,GPIO.OUT)
pwm = GPIO.PWM(servo_pin,50)
pwm.start(7)
pwm.ChangeDutyCycle(2)


drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
color=(0,0,255)
cx,cy,w,h=100,100,90,90

cap = cv2.VideoCapture(0)
count=0
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7,
                       min_tracking_confidence=0.7, max_num_hands=1) as hands:
     while True:
           ret, frame = cap.read()
           count += 1
           if count % 3 != 0:
              continue
           frame1 = cv2.resize(frame, (640, 480))
           results = hands.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
           if results.multi_hand_landmarks != None:
              for handlms in results.multi_hand_landmarks:

                  list=[]
                  for id, pt in enumerate (handlms.landmark):           
                
                      x = int(pt.x * 640)
                      y = int(pt.y * 480)
                      list.append([id ,x,y])
                  if len(list) != 0:     
                       cursor=(list)
                       cursor=list[8][1:]
                       x2,y2=list[12][1:]
                       cv2.circle(frame1,(cursor),10,(0,255,0),-1)
                       cv2.circle(frame1,(x2,y2),10,(0,0,255),-1)
                      
                       length = math.hypot(x2-cursor[0],y2-cursor[1])
                       if cx-w//2 <cursor[0]<cx+w//2 and cy-h//2<cursor[1]<cy+h//2:  
                            color=(0,255,0)
                            if length < 30:
                                 cx,cy=cursor
                                 a=(cx//2)/25
                                 print(a)
                                 pwm.ChangeDutyCycle(a)
                            else:
                                pwm.ChangeDutyCycle(0)
                                
                       else:
                            color=(0,0,255)  
                           
                          
                           
#           cv2.rectangle(frame1,(100,100),(200,200),(color),cv2.FILLED)
                          
           cv2.rectangle(frame1,(cx-w//2,cy-h//2),(cx+w//2,cy+h//2),(color),3)



                     

           cv2.imshow("Frame", frame1)
           if cv2.waitKey(1)&0xFF==27:
              break
   

cap.release()
cv2.destroyAllWindows()

