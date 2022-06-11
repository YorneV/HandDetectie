import mediapipe as mp
import cv2
import mouse
try:
    from autopy import screen
except:
    pass
try:
    from win32api import GetSystemMetrics
except:
    pass

class handDetector():
    def __init__(self, mode=False, maxHands = 2, confidence= 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.confidence = confidence

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(model_complexity=0, max_num_hands=self.maxHands, static_image_mode=self.mode, min_detection_confidence=self.confidence)

        self.cap = cv2.VideoCapture(0)
        self.index_x = None
        self.index_y = None
        self.thumb_x = None
        self.thumb_y = None
        self.middel_x = None
        self.middel_y = None
        self.distance = None

        self.prev_middel_x = 0
        self.prev_middel_y = 0
        try:
            self.width, self.height = screen.size()
            self.width, self.height = 1.5*self.width, 1.5*self.height
        except:
            pass
        try:
            self.width, self.height = GetSystemMetrics(0),GetSystemMetrics(1)
        except:
            pass
        self.clicked = False

    def webCam(self):
        while self.cap.isOpened():
            succes, image = self.cap.read()
            if not succes:
                print('Broken frame')
                #broken frames need to be skipped
                continue
            image.flags.writeable = False  # to make it quicker
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)  # process de frame

            #now we draw on top of the image
            image.flags.writeable = True #now we do want to draw on top
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks: #frames waarbij hij niks vond laten skippen
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        landmark_list=hand_landmarks,
                        image=image,
                        connections=self.mp_hands.HAND_CONNECTIONS,
                        # gwn of je lijnen der tussen wilt tekenen en kleuren enzo kiezen
                        landmark_drawing_spec=self.mp_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=self.mp_styles.get_default_hand_connections_style()
                    )
            cv2.imshow("VideoStream", cv2.flip(image,1))
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break #press q to end it
            self.cap.release

    def fingerControl(self):
        while self.cap.isOpened():
            succes, image = self.cap.read()
            if not succes:
                continue #skip broken frames
            image.flags.writeable = False  # to make it quicker
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            results = self.hands.process(image)  # process de frame
            #print(image.shape)

            if results.multi_hand_landmarks:
                self.index_x = int(results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x*image.shape[1])
                self.index_y = int(results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y*image.shape[0])

                self.thumb_x = int(results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.THUMB_TIP].x*image.shape[1])
                self.thumb_y = int(results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.THUMB_TIP].y*image.shape[0])

                self.middel_x = results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x
                self.middel_y = results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y

                self.distance = ((self.index_x-self.thumb_x)**2 + (self.index_y-self.thumb_y)**2 )**0.5
                self.movement = ((self.middel_x*image.shape[1]-self.prev_middel_x*image.shape[1])**2 + (self.middel_y*image.shape[0]-self.prev_middel_y*image.shape[0])**2 )**0.5

                self.mousecontrol()
                cv2.imshow("VideoStream", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break  # press q to end it
                self.cap.release

    def mousecontrol(self):
        threshold = 8 #amount of pixels
        thresholdclick = 20
        try:
            if self.movement > threshold: #if distance is less then threshold then probably noise
                self.middel_x = min(max(self.middel_x*(1/0.8)-(0.1/0.8), 0), 1)
                self.middel_y = min(max(self.middel_y*(1/0.8)-(0.1/0.8), 0), 1)
                mouse.move(int(self.middel_x*self.width), int(self.middel_y*self.height))
                if self.distance < thresholdclick and not self.clicked:
                    mouse.click('left')
                    print("geklikt")
                    self.clicked = True
            if self.distance > (thresholdclick + 2) and self.clicked:
                self.clicked = False   
        except:
            pass
        self.prev_middel_x, self.prev_middel_y = self.middel_x, self.middel_y


class handDetectorGrid():
    def __init__(self, mode=False, maxHands = 2, confidence= 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.confidence = confidence

        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(model_complexity=0, max_num_hands=self.maxHands, static_image_mode=self.mode, min_detection_confidence=self.confidence)

        self.cap = cv2.VideoCapture(0)
        self.index_x = None
        self.index_y = None
        self.thumb_x = None
        self.thumb_y = None
        self.wrist_x = None
        self.wrist_y = None
        self.distance = None

        self.prev_wrist_x = None
        self.prev_wrist_y = None
        try:
            self.width, self.height = screen.size()
        except:
            pass
        try:
            self.width, self.height = GetSystemMetrics(0),GetSystemMetrics(1)
        except:
            pass
        self.clicked = False

    def webCam(self):
        while self.cap.isOpened():
            succes, image = self.cap.read()
            if not succes:
                print('Broken frame')
                #broken frames need to be skipped
                continue
            image.flags.writeable = False  # to make it quicker
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            cv2.imshow("VideoStream", cv2.flip(image,1))
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break #press q to end it
            self.cap.release

    def fingerControl(self):
        while self.cap.isOpened():
            succes, image = self.cap.read()
            if not succes:
                continue #skip broken frames
            image.flags.writeable = False  # to make it quicker
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            results = self.hands.process(image)  # process de frame

            if results.multi_hand_landmarks:
                self.index_x = int(results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x*image.shape[1])
                self.index_y = int(results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y*image.shape[0])

                self.thumb_x = int(results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.THUMB_TIP].x*image.shape[1])
                self.thumb_y = int(results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.THUMB_TIP].y*image.shape[0])

                self.wrist_x = results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.WRIST].x
                self.wrist_y = results.multi_hand_landmarks[0].landmark[self.mp_hands.HandLandmark.WRIST].y

                self.distance = ((self.index_x-self.thumb_x)**2 + (self.index_y-self.thumb_y)**2 )**0.5

                self.mouseControl()
                cv2.imshow("VideoStream", cv2.flip(image,1))
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break  # press q to end it
                self.cap.release

    def mouseControl(self):
        threshold = 1/100 #it's in percentages
        thresholdclick = 20
        gridsize = 120

        try:
            if abs(self.prev_wrist_x - self.wrist_x) > threshold or abs(self.prev_wrist_y - self.wrist_y) > threshold: #if distance is less then threshold then probably noise
                self.wrist_x = min(max(self.wrist_x*(1/0.8)-(0.1/0.8), 0), 1)
                self.wrist_y = min(max(self.wrist_y*(1/0.8)-(0.1/0.8), 0), 1)
                x = self.wrist_x*self.width
                y = self.wrist_y*self.height
                for i in range(0,gridsize):
                    if round(self.width/gridsize)*(i+1) > x > round(self.width/gridsize)*(i):
                        x = round(self.width/gridsize)*(i+1) 
                    if round(self.height/gridsize)*(i+1) > y > round(self.height/gridsize)*(i):
                        y = round(self.height/gridsize)*(i+1)
                        break
                mouse.move(x, y)
            if self.distance < thresholdclick and not self.clicked:
                mouse.click('left')
                print("geklikt")
                self.clicked = True
            if self.distance > (thresholdclick + 2) and self.clicked:
                self.clicked = False   
        except:
            pass
        self.prev_wrist_x, self.prev_wrist_y = self.wrist_x, self.wrist_y

if __name__ == '__main__':
    handDetector(maxHands=2, mode=False, confidence=0.8).fingerControl()
