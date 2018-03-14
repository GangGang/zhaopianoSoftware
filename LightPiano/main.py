# -*- coding: utf-8 -*-
import tkinter
from tkinter import filedialog
from midi_analyzer import MidiAnalyzer
from key_light_maker import KeyLight
import midi
import os
import cv2
from shutil import copyfile


class App(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.root = master
        self.pack()
        self.setup()
        self.create_widgets()

    def create_widgets(self):
        self.btn0 = tkinter.Button(self.root, text='选择midi文件', command=self.open_file)
        self.label1 = tkinter.Label(self.root)
        self.btn1 = tkinter.Button(self.root, text='开始导出按键亮光视频',command=self.do_actions)
        self.label2 = tkinter.Label(self.root)
        self.btn0.pack()
        self.label1.pack()
        self.btn1.pack()
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

    def do_actions(self):
        self.analysie_midi()
        self.export_video()
root = tkinter.Tk()
app = App(master=root)


app.mainloop()

