# -*- coding: utf-8 -*-
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from midi_analyzer import MidiAnalyzer
from key_light_maker import KeyLight
import midi
import os
import cv2
from shutil import copyfile
from PIL import Image, ImageTk
import PIL
import numpy as np
import json


class FixTool(tkinter.Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.screen_height = self.parent.screenheight
        self.all_keys = {str(x):14*x for x in range(89)}    #以字典形式存储的键值对，长度89包含了按键及踏板，key：value ,key为亮光索引0～88，value为当前亮光的横坐标0～1279
        self.current_light_index = 0
        self.light_y=0
        self.bind('<Key>', self.printkey)
        self.attributes("-fullscreen", True)
        # self.update_idletasks()
        self.update_idletasks()
        self.piano_img = self.load_piano_img().convert('RGBA')
        print(self.winfo_width(),self.winfo_height())
        real_height = self.winfo_height()
        self.packUI()

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
            origin_img = Image.alpha_composite(background, png)

        resized_img = self.resize_image(origin_img, 1280)#1280*720
        return resized_img
    def add_lights(self,canvas):
        #canvas size should be 1280*720
        kl = KeyLight([], dst='', fps=1,width=1280)
        kl.draw_pic2(kl.piano_key_status[0],split_key=True,position=self.all_keys)
        tmp = kl.piano_key_status[0]
        for i,v in enumerate(tmp):
            if i != self.current_light_index:
                tmp[i] = 0
            else:
                tmp[i] = 1
        kl.draw_sentinel(tmp,position=self.all_keys)
        frame = kl.canvas
        img = PIL.Image.fromarray(frame)
        canvas.paste(img,box=(0,self.light_y))
        c = np.array(canvas)
        return c
    def clean_canvas(self):
        self.canvas = np.zeros(shape=(720,1280,4),dtype=np.uint8)
        self.canvas += 0xEB # 背景颜色
    def packUI(self):
        piano_img = self.load_piano_img().convert('RGBA')
        self.canvas = self.add_lights(piano_img)
        c = PIL.Image.fromarray(self.canvas).convert('RGB')
        img = ImageTk.PhotoImage(c)

        frm_L = tkinter.Frame(self)
        self.label = Label(frm_L, image=img)
        self.label.photo = img
        self.label.pack()
        frm_L.pack(side='left')

        frm_R = tkinter.Frame(self)
        self.label2 = Label(frm_R)
        self.label2['text'] = '请设置'
        self.label2.pack()

        self.scale1 = Scale(frm_R,from_=350,to=700,orient=HORIZONTAL,variable=self.light_y,command=self.adjust_light_y).pack()
        self.btn0 = tkinter.Button(frm_R, text='导入亮光位置文件', command=self.load_keys)
        self.btn0.pack()
        self.button1 = Button(frm_R,text='导出亮光位置文件', command=self.export_keys)
        self.button1.pack()
        frm_R.pack(side='left')
    def update_canvas(self):
        self.canvas = self.add_lights(self.piano_img)
        c = PIL.Image.fromarray(self.canvas).convert('RGB')
        img = ImageTk.PhotoImage(c)
        self.label.configure(image=img)
        self.label.photo = img
        # self.canvas = None
        self.clean_canvas()
    def update_index(self,plus=1):
        #更新亮光索引
        self.current_light_index += plus
        if self.current_light_index > 88-1:
            self.current_light_index = 0
        if self.current_light_index < 0:
            self.current_light_index = 88-1
    def update_key_position(self,key_index,plus=1):
        for i in range(key_index,len(self.all_keys)):
            if i >= key_index:
                self.all_keys[str(i)]+=plus
    def update_single_key_position(self,key_index,plus=1):
        self.all_keys[str(key_index)]+=plus
    def adjust_light_y(self,v):
        self.light_y = int(v)
        self.update_canvas()
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
        self.update_canvas()
    def export_keys(self):
        json_str = json.dumps(self.all_keys)
        name = filedialog.asksaveasfilename(title='保存文件', initialdir='./', initialfile='light_key.json')
        f = open(name,mode='w')
        f.write(json_str)
        f.close()
        messagebox.showinfo('','配置文件保存完成！')
    def load_keys(self):
        filename = filedialog.askopenfilename()
        print(filename)
        f = open(filename,mode='r')
        json_str = f.read()
        self.all_keys = json.loads(json_str)
        f.close()
        self.update_canvas()
class App(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.root = master
        self.pack()
        self.setup()
        self.create_widgets()

    def create_widgets(self):
        self.btn1 = tkinter.Button(self.root, text='选择midi文件', command=self.open_file);self.btn1.pack()
        self.label1 = tkinter.Label(self.root);self.label1.pack()
        self.btn4 = tkinter.Button(self.root, text='选择亮光位置配置json文件', command=self.load_keys);self.btn4.pack()
        self.label4 = tkinter.Label(self.root);self.label4.pack()
        self.btn2 = tkinter.Button(self.root, text='开始导出按键亮光视频', command=self.do_actions);self.btn2.pack()
        self.label2 = tkinter.Label(self.root);self.label2.pack()
        self.btn3 = tkinter.Button(self.root,text='修正亮光位置',command=self.show_fixtool);self.btn3.pack()


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
    def load_keys(self):
        filename = filedialog.askopenfilename()
        print(filename)
        f = open(filename,mode='r')
        json_str = f.read()
        self.all_keys = json.loads(json_str)
        f.close()
        self.label4['text'] = '配置文件载入完毕：'+filename
    def export_video(self):
        output_dir = os.path.dirname(self.file_path)
        origin_file_name = os.path.basename(self.file_path).split('.')[-2]
        output_file_name = output_dir+'/'+origin_file_name+'.mp4'
        output_tmp_file_name = output_dir+'/tmp_keylight_video.mp4'
        if os.path.isfile(output_tmp_file_name):
            os.remove(output_tmp_file_name)
        if os.path.isfile(output_file_name):
            os.remove(output_file_name)
        frame_width = 1280

        kl = KeyLight(piano_key_status=self.piano_key_status,
                      dst = output_tmp_file_name,
                      width=frame_width,
                      fps=self.fps,
                      position=self.all_keys)
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

