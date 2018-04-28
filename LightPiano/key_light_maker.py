import cv2
import numpy as np
from PIL import Image
import os
class KeyLight():
    def __init__(self,piano_key_status,dst,width=1280,fps=30):
        self.canvas_width = width
        self.canvas_height = int(width*0.05)
        if self.canvas_height%2 !=0:
            self.canvas_height+=1
        self.clean_canvas()
        self.key_width = int(self.canvas_width/88)
        self.piano_key_status = piano_key_status
        self.fps = fps
        self.dst = dst
        self.add_examine_status()
        spot = cv2.imread('spot1.png',flags=-1)
        self.spot = cv2.resize(spot, dsize=(int(self.key_width), int(self.key_width)))
        ped = cv2.imread('ped.png',flags=-1)
        h, w, _ = ped.shape
        h_ = self.key_width
        w_ = (w / h) * h_
        self.ped = cv2.resize(ped, dsize=(int(w_), int(h_)))

    def draw(self,status):
        self.clean_canvas()
        for i,key in enumerate(status):
            center = (int((i+1/2)*self.key_width),int(self.canvas_height/2))
            radius = int((self.key_width * 0.8)/2)
            if key < 0:
                cv2.circle(self.canvas,center,radius,color=(0),thickness=-1)
            else:
                cv2.circle(self.canvas,center,radius,color=(0,255,0),thickness=-1)
    def draw_pic(self,status):
        self.clean_canvas()
        key_status = status[0:-1]# first 88 keys
        pedal_status = status[-1]
        for i,key in enumerate(key_status):

            if key > 0:
                y1 = int((self.canvas_height- self.key_width))
                y2 = y1 + self.key_width
                x1 = int(i*self.key_width)
                x2 = int((i+1)*self.key_width)
                bg = Image.fromarray(self.canvas)
                s = Image.fromarray(self.spot)
                bg.paste(s,box=(x1,y1),mask=s)
                self.canvas = np.array(bg)
            else:
                pass
                # cv2.circle(self.canvas,center,radius,color=(0,255,0),thickness=-1)

        if pedal_status > 0:
            # center = (int((len(key_status)-1+1/2)*self.key_width),int(self.canvas_height/2))
            # radius = int((self.key_width * 0.8)/2)
            # cv2.circle(self.canvas, center, radius, color=(0, 255, 0), thickness=-1)
            bg = Image.fromarray(self.canvas)
            s = Image.fromarray(self.ped)
            bg.paste(s, box=(int((len(key_status)-3)*self.key_width),int(self.canvas_height*0.3)), mask=s)
            self.canvas = np.array(bg)

    def clean_canvas(self):
        self.canvas = np.zeros(shape=(self.canvas_height,self.canvas_width,4),dtype=np.uint8)
        self.canvas += 0xEB # 背景颜色
    def add_examine_status(self):
        examine_status = [1]*len(self.piano_key_status[0])
        for i in range(self.fps):
            self.piano_key_status.insert(0,examine_status)
    def run(self):
        # fourcc = cv2.VideoWriter_fourcc(*'X264')# X264 quality is better than MJPG
        out = cv2.VideoWriter(self.dst, 0x00000021, self.fps, (self.canvas_width, self.canvas_height))
        for s in self.piano_key_status:
            self.draw_pic(s)
            frame = self.canvas
            out.write(frame)
        out.release()
