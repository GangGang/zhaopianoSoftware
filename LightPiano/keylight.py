# -*- coding:utf-8 -*-

import cv2
import numpy as np
import json
class KeyLight():
    def __init__(self,width=1280):
        self.canvas_width = width
        self.canvas_height = int(width*0.03)
        self.canvas = np.zeros(shape=(self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.canvas += 255
        self.key_width = int(self.canvas_width/88)
    def draw(self,status):
        self.canvas = np.zeros(shape=(self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.canvas += 255
        for i,key in enumerate(status):
            center = (int((i+1/2)*self.key_width),int(self.canvas_height/2))
            radius = int((self.key_width * 0.8)/2)
            if key < 0:
                cv2.circle(self.canvas,center,radius,color=(0),thickness=-1)
            else:
                cv2.circle(self.canvas,center,radius,color=(0,255,0),thickness=-1)
    def draw_pic(self,status):
        self.canvas = np.zeros(shape=(self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.canvas += 255
        spot = cv2.imread('spot1.png')
        spot = spot.resize(dsize=(int(self.key_width * 0.8),int(self.key_width * 0.8)))
        for i,key in enumerate(status):
            center = (int((i+1/2)*self.key_width),int(self.canvas_height/2))
            radius = int((self.key_width * 0.8)/2)
            if key < 0:
                cv2.circle(self.canvas,center,radius,color=(0),thickness=-1)
            else:
                cv2.circle(self.canvas,center,radius,color=(0,255,0),thickness=-1)
                # self.canvas[self.key_width-:y2, int(i*self.key_width):int((i+1)*self.key_width)] = spot
if __name__ == '__main__':
    tps = 679
    f = open('tps'+str(tps)+'.json')
    txt = f.read()
    f.close()
    o = json.loads(txt)
    print('start')

    kl = KeyLight(width=1920)
    fps = 30
    # cap = cv2.VideoCapture(0)

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('tps_new'+str(tps)+'.mp4', fourcc, fps, (1920, 57))


    # Release everything if job is finished

    for s in o:
        kl.draw(s)
        # ret, frame = cap.read()
        frame2 = kl.canvas
        # cv2.VideoWriter()
        # cv2.imshow('ke',kl.canvas)
        # cv2.waitKey(int(1000/60))
        out.write(frame2)

    out.release()

