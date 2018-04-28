#!/usr/bin/python2.6
# -*- coding: utf-8 -*-
# 此app用来生成宝贝详情图
import tkinter
from tkinter import filedialog
from tkinter import ttk

import xml.etree.ElementTree as ET
import os
from PIL import Image,ImageDraw
from utils import image_stitch,add_text,load_images
import argparse
import os.path
import shutil
CANVAS_WIDTH = 1100
IMAGE_RATIO = 0.9
IMAGE_WIDTH = int(IMAGE_RATIO*CANVAS_WIDTH)
BLOCK_GAP = int((1-IMAGE_RATIO)*CANVAS_WIDTH/2)

EXPORT_HEIGHT = 1920
class Canvas():
    def __init__(self,width):
        self.bg = self.formatImage(Image.open('bg6.jpg'),new_w=CANVAS_WIDTH)[0]
        self.exported_images = []

    def append(self,image,round_corner = -1):
        image, mask = self.formatImage(image,round_corner=round_corner)
        validbg = self.validBg(image.height+BLOCK_GAP)
        new_bg = validbg.crop(box=(0, 0, CANVAS_WIDTH-1, image.height+BLOCK_GAP))
        new_bg.paste(image,(BLOCK_GAP,int(BLOCK_GAP/2)),mask=mask)
        self.exported_images.append(new_bg)

    # 格式化图片
    def formatImage(self,img,new_w = IMAGE_WIDTH,round_corner = -1):
        # new_w = IMAGE_WIDTH
        new_h = int((new_w/img.width)*img.height)
        new_img = img.resize(size=(new_w,new_h),resample= Image.BILINEAR)

        if round_corner > 0:
            mask = Image.new(mode='L',size=new_img.size) # 8bit灰度图
            draw = ImageDraw.Draw(mask)
            d = 2*round_corner
            w,h = mask.width,mask.height
            draw.ellipse(xy=[0,0,d,d],fill=(255))
            draw.ellipse(xy=[mask.width-1-d,0,mask.width-1,d],fill=(255))
            draw.ellipse(xy=[0,mask.height-d,d,mask.height],fill=(255))
            draw.ellipse(xy=[mask.width-1-d,mask.height-d,mask.width-1,mask.height],fill=(255))

            draw.rectangle(xy=[d/2,0,w-d/2,h],fill=255)
            draw.rectangle(xy=[0,d/2,w,h-d/2],fill=255)
            # mask.show()
        else:
            mask = new_img
        return new_img,mask

    #确保背景高度足够
    def validBg(self,asked_height):
        i=2
        bg = self.bg
        while asked_height>bg.height:
            new_bg = Image.new('RGB',size=(self.bg.width,self.bg.height*i))
            new_bg.paste(bg,box=(0,0))
            new_bg.paste(self.bg,box=(0,self.bg.height*(i-1)))
            bg = new_bg
            i+=1
        return bg

    def export(self,save_to_disk = "",preview_only=False):
        if save_to_disk != "":
            if os.path.exists(save_to_disk):
                shutil.rmtree(save_to_disk)
            os.mkdir(save_to_disk)
            if preview_only:
                self.exported_images[1].save(save_to_disk + '/淘宝图' + str(1) + '.jpg', quality=100)
            else:
                for key,item in enumerate(self.exported_images):
                    item.save(save_to_disk+'/淘宝图'+str(key)+'.jpg',quality=100)
class App(tkinter.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.root = master
        self.pack()
        self.setup()
        self.create_widgets()

    def create_widgets(self):
        self.btn0 = tkinter.Button(self.root, text='选择乐谱jpg文件', command=self.open_file)
        self.btn0.pack()
        self.label1 = tkinter.Label(self.root)
        self.label1.pack()

        # left
        frm = tkinter.Frame(self.root)
        frm_L = tkinter.Frame(frm)
        tkinter.Label(frm_L, text="请选择谱子总页数：").pack()
        frm_L.pack(side='left')
        # right
        frm_R = tkinter.Frame(frm)
        comvalue = tkinter.StringVar()  # 窗体自带的文本，新建一个值
        comboxlist = ttk.Combobox(frm_R, textvariable=comvalue)  # 初始化
        comboxlist["values"] = ("1", "2", "3", "4",'5','6','7','8')
        comboxlist['state'] = 'readonly'
        comboxlist.current(0)  # 选择第一个
        comboxlist.bind("<<ComboboxSelected>>",self.set_pages )  # 绑定事件,(下拉列表框被选中时，绑定go()函数)
        self.comboxlist = comboxlist
        self.comboxlist.pack()
        frm_R.pack(side='right')
        frm.pack()  # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM

        self.export_preview_only = tkinter.BooleanVar()
        self.export_preview_only.set(1)
        print(self.export_preview_only.get())
        self.checkb = tkinter.Checkbutton(self.root, text = "仅输出谱子预览页", variable = self.export_preview_only)
        self.checkb.pack()

        self.btn1 = tkinter.Button(self.root, text='开始生成宝贝详情页',command=self.do_actions)
        self.btn1.pack()
        self.label2 = tkinter.Label(self.root)
        self.label2.pack()
    def set_pages(self,event):
        self.total_pages = self.comboxlist.get()

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
        self.root.title('美美老师请尽情使用我吧 之 淘宝宝贝详情生成工具')

    def open_file(self):
        filename = filedialog.askopenfilename()
        print('文件名已加载',filename)
        self.label1['text'] = filename
        self.jpg_file_path = filename
    def do_actions(self):
        self.stitch_images()
        # self.export_file()
    def stitch_images(self):
        IMAGES_LIST = [
            '淘宝/信.png',
            '淘宝/淘宝图1：放大镜1.jpg',
            '淘宝/淘宝图2：打印效果.jpg',
            '淘宝/淘宝图3：PDF+JPG.jpg',
            '淘宝/淘宝图4：指法标注.jpg',
            '淘宝/淘宝图5：教学视频.jpg',
            '淘宝/淘宝图6：演奏音频.jpg',
            # '淘宝/淘宝图7：粉丝群.jpg',
            '淘宝/淘宝图8：发货说明.jpg',
            '淘宝/淘宝图9：五星好评.jpg'
        ]
        # parser = argparse.ArgumentParser()
        # parser.add_argument('score_file', help='请输入乐谱第一页的文件路径', type=str)
        # parser.add_argument('pages', help='请输入全谱页数', type=str)
        # parser.add_argument('--nofinger', help='添加此参数表示不输出指法页', action='store_true')
        # parser.add_argument('--novideo', help='添加此参数表示不输出教学视频页', action='store_true')
        # parser.add_argument('--noaudio', help='添加此参数表示不输出演奏音频页', action='store_true')
        # args = parser.parse_args()
        file_name = os.path.basename(self.jpg_file_path).split('.')[-2]
        output_dir = os.path.dirname(self.jpg_file_path) + '/' + str(file_name)

        score_title = Image.open('淘宝/淘宝图0：乐谱预览.jpg')
        score_img = Image.open(self.jpg_file_path)
        score_bottom = Image.open('淘宝/淘宝图10：blank.jpg')

        # if args.nofinger:
        #     IMAGES_LIST.remove('淘宝/淘宝图4：指法标注.jpg')
        # if args.novideo:
        #     IMAGES_LIST.remove('淘宝/淘宝图5：教学视频.jpg')
        # if args.noaudio:
        #     IMAGES_LIST.remove('淘宝/淘宝图6：演奏音频.jpg')
        imgs = load_images(IMAGES_LIST)
        c = Canvas(CANVAS_WIDTH)

        score_bottom = add_text(score_bottom, '全谱共' + self.total_pages + '页', '汉仪小麦体简.ttf')

        score = image_stitch(score_title, score_img)
        score = image_stitch(score, score_bottom)
        imgs.insert(1, score)

        for key, img in enumerate(imgs):
            if key == 0:# first page
                c.append(img)
            else:
                c.append(img, round_corner=50)
        print(self.export_preview_only.get())
        c.export(save_to_disk=output_dir,preview_only=self.export_preview_only.get())
        self.label2['text'] = '图片生成成功,文件存储在：\n'+output_dir

root = tkinter.Tk()
app = App(master=root)
app.mainloop()
