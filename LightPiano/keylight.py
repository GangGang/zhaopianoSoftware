# -*- coding:utf-8 -*-

import cv2
import numpy as np
import json
from PIL import Image,ImageDraw

class KeyLight():
    def __init__(self,width=1280):
        self.canvas_width = width
        self.canvas_height = int(width*0.03)
        self.canvas = np.zeros(shape=(self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.canvas += 0xEB
        self.key_width = int(self.canvas_width/88)
    def draw(self,status):
        self.canvas = np.zeros(shape=(self.canvas_height,self.canvas_width,3),dtype=np.uint8)
        self.canvas += 0xEB
        for i,key in enumerate(status):
            center = (int((i+1/2)*self.key_width),int(self.canvas_height/2))
            radius = int((self.key_width * 0.8)/2)
            if key < 0:
                cv2.circle(self.canvas,center,radius,color=(0),thickness=-1)
            else:
                cv2.circle(self.canvas,center,radius,color=(0,255,0),thickness=-1)
    def draw_pic(self,status):
        self.canvas = np.zeros(shape=(self.canvas_height,self.canvas_width,4),dtype=np.uint8)
        self.canvas += 255
        spot = cv2.imread('spot1.png',flags=-1)
        spot = cv2.resize(spot,dsize=(int(self.key_width),int(self.key_width)))
        for i,key in enumerate(status):
            if key > 0:
                y1 = int((self.canvas_height- self.key_width)/2)
                y2 = y1 + self.key_width
                x1 = int(i*self.key_width)
                x2 = int((i+1)*self.key_width)
                bg = Image.fromarray(self.canvas)
                s = Image.fromarray(spot)
                bg.paste(s,box=(x1,y1),mask=s)
                self.canvas = np.array(bg)

if __name__ == '__main__':
    tps = 679
    frame_width = 1280
    f = open('tps'+str(tps)+'.json')
    txt = f.read()
    f.close()
    o = json.loads(txt)
    print('start')

    kl = KeyLight(width=frame_width)
    fps = 30

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('tps'+str(tps)+'.mp4', fourcc, fps, (kl.canvas_width, kl.canvas_height))

    for s in o:
        kl.draw_pic(s)
        frame2 = kl.canvas
        out.write(frame2)

    out.release()

