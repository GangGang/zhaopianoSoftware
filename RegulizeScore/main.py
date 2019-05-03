#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
import tkinter
from tkinter import filedialog
import xml.etree.ElementTree as ET
import os
from util import regulize_image,export_file
class App(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.root = master
        self.pack()
        self.setup()
        self.create_widgets()

    def create_widgets(self):
        self.btn0 = tkinter.Button(self.root, text='选择已切割png乐谱目录', command=self.open_xmlfile)
        self.label1 = tkinter.Label(self.root)
        self.btn1 = tkinter.Button(self.root, text='开始对齐',command=self.do_actions)
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
        self.root.title('美美老师请尽情使用我吧')

    def open_xmlfile(self):
        dir_name = filedialog.askdirectory()
        print(dir_name)
        self.dir_path = dir_name
        self.label1['text'] = dir_name
    def get_tree(self):
        self.tree = ET.parse(self.xml_file_path)
        self.tree_root = self.tree.getroot()
    def add_staves(self):
        r = self.tree_root.findall('.//attributes')# find all attributes nodes
        el = ET.Element('staves')
        el.text = '2'
        for node in r:
            node.insert(0,el)
    def do_actions(self):
        dst = export_file(self.dir_path)
        self.label2['text'] = "完成,新图像存储在："+dst

root = tkinter.Tk()
app = App(master=root)


app.mainloop()

