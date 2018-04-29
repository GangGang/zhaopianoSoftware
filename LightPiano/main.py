# -*- coding: utf-8 -*-
import tkinter
from tkinter import *
from tkinter import filedialog
from midi_analyzer import MidiAnalyzer
from key_light_maker import KeyLight
import midi
import os
import cv2
from shutil import copyfile
from PIL import Image, ImageTk
import PIL
import numpy as np
class FixTool(tkinter.Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.screen_height = self.parent.screenheight
        self.all_keys = {x:14*x for x in range(88)}    #以字典形式存储的键值对，key：value ,key为亮光索引0～87，value为当前亮光的横坐标0～1279
        self.current_light_index = 0
        self.bind('<Key>', self.printkey)
        self.attributes("-fullscreen", True)
        # self.update_idletasks()
        print(self.winfo_width(),self.winfo_height())
        real_height = self.winfo_height()
        self.packUI()
        self.update_idletasks()

    def resize_image(self,img,target_width):
        w, h = img.size
        w_new = int(target_width)
        h_new = int((h / w) * w_new)
        resized_img = img.resize((w_new, h_new),resample=Image.BILINEAR)
        return resized_img
    def load_piano_img(self):
        origin_img = Image.open('./piano_img.png')
        if origin_img.mode == 'RGBA':
            png = origin_img
            background = Image.new('RGBA', png.size, (255, 255, 255))
            alpha_composite = Image.alpha_composite(background, png)
            origin_img = alpha_composite

        resized_img = self.resize_image(origin_img, 1280)#1280*720
        return resized_img
    def add_lights(self,canvas):
        #canvas size should be 1280*720
        kl = KeyLight([], dst='', fps=1,width=1280)
        kl.draw_pic2(kl.piano_key_status[0],split_key=True,position=self.all_keys)
        frame = kl.canvas
        img = PIL.Image.fromarray(frame)
        canvas.paste(img)
        c = np.array(canvas)
        return c
    def packUI(self):
        piano_img = self.load_piano_img().convert('RGBA')
        self.canvas = self.add_lights(piano_img)
        c = PIL.Image.fromarray(self.canvas).convert('RGB')
        img = ImageTk.PhotoImage(c)
        # img = self.canvas
        # _,w = img._PhotoImage__size
        # w = int(img._PhotoImage__size[0])
        # frm_0 = tkinter.Frame(self,width=w)
        # frm_0.pack(side='left')

        frm_L = tkinter.Frame(self)
        self.label = Label(frm_L, image=img)
        self.label.photo = img
        self.label.pack()
        frm_L.pack(side='left')

        frm_R = tkinter.Frame(self)
        self.label2 = Label(frm_R)
        self.label2['text'] = '请设置'
        self.label2.pack()
        frm_R.pack(side='left')
    def update_index(self,plus=1):
        #更新亮光索引
        self.current_light_index += plus
        if self.current_light_index > 88-1:
            self.current_light_index = 0
        if self.current_light_index < 0:
            self.current_light_index = 88-1
    def update_key_position(self,key_index,plus=1):
        self.all_keys[key_index]+=plus
    def printkey(self,event):
        print('你按下了: ' + event.char,'keycode:',event.keycode)# <KeyPress event state=Mod3 keysym=KP_Enter keycode=4980739 char='\x03' delta=4980739 x=-776 y=-53>
        print(event)
        next_light_keys=['Down']
        previous_light_keys=['Up']
        move_right_keys = ['Right']
        move_left_keys = ['Left']
        exit_keys = ['Escape']
        if(event.keysym in next_light_keys):
            self.update_index(plus=1)
            print('当前琴键：', self.current_light_index)
        elif(event.keysym in previous_light_keys):
            self.update_index(plus=-1)
            print('当前琴键：', self.current_light_index)
        elif(event.keysym in move_right_keys):
            self.update_key_position(key_index=self.current_light_index,plus=1)
            print('亮光右移')
        elif(event.keysym in move_left_keys):
            self.update_key_position(key_index=self.current_light_index,plus=-1)
            print('亮光左移')

        elif(event.keysym in exit_keys):
            self.destroy()
        # img = ImageTk.PhotoImage(self.all_scores[self.current_light_index])
        # self.label.configure(image=img)
        # self.label.photo = img
        #
        # img2 = ImageTk.PhotoImage(self.all_scores[self.current_light_index + 1])
        # self.label2.configure(image=img2)
        # self.label2.photo = img2
    # def setup(self):
    #     self.center_window(self.root, 600, 300)
    #     self.root.minsize(300, 300)
    #     self.root.maxsize(600, 600)
    #     self.root.title('亮光位置修复工具')
    # def center_window(self,root, width, height):
    #     screenwidth = root.winfo_screenwidth()
    #     screenheight = root.winfo_screenheight()
    #     size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    #     print(size)
    #     root.geometry(size)
class App(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.root = master
        self.pack()
        self.setup()
        self.create_widgets()

    def create_widgets(self):
        self.btn1 = tkinter.Button(self.root, text='选择midi文件', command=self.open_file).pack()
        self.label1 = tkinter.Label(self.root).pack()
        self.btn2 = tkinter.Button(self.root, text='开始导出按键亮光视频', command=self.do_actions).pack()
        self.label2 = tkinter.Label(self.root).pack()
        self.btn3 = tkinter.Button(self.root,text='修正亮光位置',command=self.show_fixtool).pack()


    def get_screen_size(self,window):
        return window.winfo_screenwidth(), window.winfo_screenheight()

    def get_window_size(self,window):
        return window.winfo_reqwidth(), window.winfo_reqheight()

    def center_window(self,root, width, height):
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        self.screenheight = screenheight
        size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        print(size)
        root.geometry(size)

    def setup(self):
        self.center_window(self.root, 600, 300)
        self.root.minsize(300, 300)
        self.root.maxsize(600, 600)
        self.root.title('美美老师请尽情使用我吧 之 琴键亮点生成工具')

    def open_file(self):
        filename = filedialog.askopenfilename()
        print(filename)
        self.label1['text'] = filename
        self.file_path = filename
    def analysie_midi(self):
        pattern = midi.read_midifile(self.file_path)
        ma = MidiAnalyzer(pattern)
        self.piano_key_status = ma.run()
        self.fps = ma.fps
    def export_video(self):
        output_dir = os.path.dirname(self.file_path)
        origin_file_name = os.path.basename(self.file_path).split('.')[-2]
        output_file_name = output_dir+'/'+origin_file_name+'.mp4'
        output_tmp_file_name = output_dir+'/tmp_keylight_video.mp4'
        if os.path.isfile(output_tmp_file_name):
            os.remove(output_tmp_file_name)
        if os.path.isfile(output_file_name):
            os.remove(output_file_name)
        frame_width = 1920#1280

        kl = KeyLight(piano_key_status=self.piano_key_status,dst = output_tmp_file_name,width=frame_width,fps=self.fps)
        kl.run()

        copyfile(output_tmp_file_name, output_file_name)
        if os.path.isfile(output_tmp_file_name):
            os.remove(output_tmp_file_name)
        self.label2['text'] = '视频导出完成,文件存储为：\n'+output_file_name
    def show_fixtool(self):
        fix_tool = FixTool(self)
        self.wait_window(fix_tool)
    def do_actions(self):
        self.analysie_midi()
        self.export_video()
root = tkinter.Tk()
app = App(master=root)


app.mainloop()

