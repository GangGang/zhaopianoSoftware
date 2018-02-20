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
        self.load_scores()
        self.packUI()
    def update_index(self):
        if self.current_score_index == len(self.score_list)-1:
            self.current_score_index = 0
        else:
            self.current_score_index += 1

    def printkey(self,event):
        # print('你按下了: ' + event.char,'keycode:',event.keycode)# <KeyPress event state=Mod3 keysym=KP_Enter keycode=4980739 char='\x03' delta=4980739 x=-776 y=-53>
        # print(event)
        if(event.keysym=='KP_Enter'):
            self.update_index()
            print('next page ',self.current_score_index)
            # origin_img = Image.open(self.score_list[self.current_score_index])
            # resized_img = self.resize_image(origin_img)
            img = ImageTk.PhotoImage(self.all_scores[self.current_score_index])
            self.label.configure(image=img)
            self.label.photo = img

    def setup(self):
        self.parent.center_window(self, 600, 300)
        self.parent.root.minsize(300, 300)
        # self.parent.root.maxsize(600, 600)
        self.parent.root.title('乐谱查看')
    def load_scores(self):
        for item in self.score_list:
            origin_img = Image.open(item)
            resized_img = self.resize_image(origin_img)
            self.all_scores.append(resized_img)
    def resize_image(self,img):
        w, h = img.size
        h_new = int(self.screen_height)
        w_new = int((w / h) * h_new)
        resized_img = img.resize((w_new, h_new))
        return resized_img
    def packUI(self):
        # origin_img = Image.open(self.score_list[self.current_score_index])
        # resized_img = self.resize_image(origin_img)
        img = ImageTk.PhotoImage(self.all_scores[self.current_score_index])
        self.label = Label(self, image=img)
        self.label.photo = img
        self.label.pack()


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
            if item.split('.')[-1] == 'jpg':
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

