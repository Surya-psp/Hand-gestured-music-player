from pygame import mixer
import cv2
import mediapipe as mp
import time
import os


mixer.init()
path = "D:\\Songs"
# songs = os.listdir(path)
# print(songs)
songs = []
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.mp3'):
            songs.append(file)

print(songs)
index = 0
def start():
    global index
    mixer.music.load(path+"\\"+str(songs[index]))
    mixer.music.set_volume(0.3)
    mixer.music.play()

def next():
    global index
    index+=1
    start()

def prev():
    global index
    index-=1
    start()

# while True:
#     print("press 'p' to pause, 'r' to resume")
#     print("press 'e' to exit")
    # query = input("    ")
    # if query == 'p':
def pause():
    mixer.music.pause()
    # elif query == 'r':
def resume():
    mixer.music.unpause()
    # elif query == 'e':
def exit():
        mixer.music.stop()
        # break




cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
cTime, pTime = 0, 0

while True:
    li = [[], [], [], []]
    tb = 0
    fc = 4
    re = [False, False, False, False]
    success, img = cap.read()
    cap.set(10, 100)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    if results.multi_hand_landmarks:
        for handlmk in results.multi_hand_landmarks:
            for id, lm in enumerate(handlmk.landmark):
                h, w, c = img.shape
                px, py = int(lm.x*w), int(lm.y*h)
                # print(id, px, py)
                if id==4:
                    tb=py
                if id==5:
                    li[0].append(py)
                if id==8:
                    li[0].append(py)
                if id==9:
                    li[1].append(py)
                if id==12:
                    li[1].append(py)
                if id==13:
                    li[2].append(py)
                if id==16:
                    li[2].append(py)
                if id==17:
                    li[3].append(py)
                if id==20:
                    li[3].append(py)
            if tb/li[0][1]>0.9 and tb/li[0][1]<1.1:
                prev()
                # print("Yes. It is success...")
            if tb/li[2][1]>0.9 and tb/li[2][1]<1.1:
                next()
            for i in range(len(li)):
                if li[i][1]>li[i][0]:
                    re[i] = True
                    fc-=1
            # print(fc)
            # if False not in re:
            #     quit()
            if tb/li[1][1]>0.9 and tb/li[1][1]<1.1:
                pause()
            elif tb/li[3][0]>0.9 and tb/li[3][0]<1.1:
                resume()
            elif tb/li[3][1]>0.9 and tb/li[3][1]<1.1:
                exit()
            elif fc==0:
                print(111)
                start()
            fc=4
            
            mpDraw.draw_landmarks(img, handlmk, mpHands.HAND_CONNECTIONS)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 3, cv2.FILLED)
    cv2.imshow('image', img)
    cv2.waitKey(1)