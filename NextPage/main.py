#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
# 此app用来给美美老师方便翻页看乐谱用
import tkinter
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class ScoreViewer(tkinter.Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.screen_height = self.parent.screenheight
        self.score_list = self.parent.score_list
        self.all_scores = []
        self.current_score_index = 0
        print('load:',parent.score_dir)
        # self.setup()
        self.bind('<Key>', self.printkey)
        self.attributes("-fullscreen", True)
        self.update_idletasks()
        print(self.winfo_width(),self.winfo_height())
        real_height = self.winfo_height()
        self.all_scores = []
        self.load_scores(height=real_height)
        self.packUI()

    def update_index(self,plus=1):
        #更新图片索引
        self.current_score_index += plus
        if self.current_score_index > len(self.score_list)-1:
            self.current_score_index = 0
        if self.current_score_index < 0:
            self.current_score_index = len(self.score_list)-1

    def printkey(self,event):
        print('你按下了: ' + event.char,'keycode:',event.keycode)# <KeyPress event state=Mod3 keysym=KP_Enter keycode=4980739 char='\x03' delta=4980739 x=-776 y=-53>
        print(event)
        next_page_keys=['KP_Enter','Right']
        previous_page_keys=['Left']
        exit_keys = ['Escape']
        if(event.keysym in next_page_keys):
            self.update_index(plus=2)
            print('next page ',self.current_score_index)
        elif(event.keysym in previous_page_keys):
            self.update_index(plus=-2)
            print('previous page ',self.current_score_index)
        elif(event.keysym in exit_keys):
            self.destroy()
        img = ImageTk.PhotoImage(self.all_scores[self.current_score_index])
        self.label.configure(image=img)
        self.label.photo = img

        img2 = ImageTk.PhotoImage(self.all_scores[self.current_score_index+1])
        self.label2.configure(image=img2)
        self.label2.photo = img2

    def load_scores(self,height):
        for item in self.score_list:
            origin_img = Image.open(item)
            if origin_img.mode == 'RGBA':
                png = origin_img
                background = Image.new('RGBA', png.size, (255, 255, 255))
                alpha_composite = Image.alpha_composite(background, png)
                origin_img = alpha_composite

            resized_img = self.resize_image(origin_img,height)
            self.all_scores.append(resized_img)
        if int(len(self.all_scores))%2 != 0:
            white_img = Image.new('RGB', self.all_scores[0].size, (255, 255, 255))
            self.all_scores.append(white_img)

    def resize_image(self,img,target_height):
        w, h = img.size
        h_new = int(target_height)
        w_new = int((w / h) * h_new)
        resized_img = img.resize((w_new, h_new),resample=Image.BILINEAR)
        return resized_img
    def packUI(self):
        img = ImageTk.PhotoImage(self.all_scores[self.current_score_index])
        img2 = ImageTk.PhotoImage(self.all_scores[self.current_score_index+1])

        # _,w = img._PhotoImage__size
        w = int((self.winfo_width() - 2*img._PhotoImage__size[0])/2)
        frm_0 = tkinter.Frame(self,width=w)
        frm_0.pack(side='left')

        frm_L = tkinter.Frame(self)
        self.label = Label(frm_L, image=img)
        self.label.photo = img
        self.label.pack()
        frm_L.pack(side='left')

        frm_R = tkinter.Frame(self)
        self.label2 = Label(frm_R, image=img2)
        self.label2.photo = img2
        self.label2.pack()
        frm_R.pack(side='left')


class App(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.root = master
        self.pack()
        self.setup()
        self.pack_UI()


    def pack_UI(self):
        self.btn0 = tkinter.Button(self.root, text='选择含有乐谱图片的文件夹', command=self.load_scores)
        self.btn0.pack()
        self.label1 = tkinter.Label(self.root)
        self.label1.pack()
        self.btn1 = tkinter.Button(self.root, text='开始显示曲谱！！',command=self.do_actions)
        self.btn1.pack()
        self.label2 = tkinter.Label(self.root)
        self.label2.pack()

    def get_screen_size(self,window):
        return window.winfo_screenwidth(), window.winfo_screenheight()

    def get_window_size(self,window):
        return window.winfo_reqwidth(), window.winfo_reqheight()

    def center_window(self,root, width, height):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        print(size)
        root.geometry(size)
        self.screenheight = screenheight

    def setup(self):
        self.center_window(self.root, 600, 300)
        self.root.minsize(300, 300)
        self.root.maxsize(600, 600)
        self.root.title('美美老师请尽情使用我吧')

    def load_scores(self):
        filename = filedialog.askdirectory()
        print(filename)
        self.label1['text'] = filename
        self.score_dir = filename
        r = os.listdir(self.score_dir)
        score_list = []
        for item in r:
            if item.split('.')[-1] == 'jpg'or item.split('.')[-1] =='png':
                score_list.append(self.score_dir+'/'+item)
        print(r)
        print(score_list)
        self.score_list = score_list
    def show_scores(self):
        score_viewer = ScoreViewer(self)
        self.wait_window(score_viewer)
    def do_actions(self):
        self.show_scores()


root = tkinter.Tk()
app = App(master=root)


app.mainloop()

