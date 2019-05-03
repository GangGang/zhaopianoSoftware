'''
将手工裁切的png乐谱行图像归一化为同一高度。
'''

import cv2,os,shutil
import numpy as np

def get_dir_filelist_by_extension(dir, ext):
    r = os.listdir(dir)
    file_list = []
    for item in r:
        if item.split('.')[-1] == ext:
            file_list.append(dir + '/' + item)
    return file_list
def get_parent_dir(dir):
    parent_dir, tail = os.path.split(os.path.abspath(dir))  # 使用abspath函数先规范化路径
    return parent_dir,tail
def create_new_empty_dir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.mkdir(dir)
    return dir
def regulize_image(image_path,fix_pos):
    template = cv2.imread("template.png",flags=cv2.IMREAD_UNCHANGED)
    image = cv2.imread(image_path,flags=cv2.IMREAD_UNCHANGED)
    image_height = image.shape[0]
    bg = np.zeros(shape=(int((9/16)*image.shape[1]),image.shape[1],image.shape[2]),dtype=image.dtype)
    result = cv2.matchTemplate(image,template,cv2.TM_SQDIFF,mask=template)
    loc = cv2.minMaxLoc(result)
    pos_y = loc[3][1]
    pos = fix_pos - pos_y
    bg[pos:pos+image_height,:] = image
    final = cv2.resize(bg,(1920,1080),interpolation=cv2.INTER_LINEAR_EXACT)
    return final
def export_file(origin_dir):

    file_list = get_dir_filelist_by_extension(origin_dir,"png")
    parent_dir,_ =get_parent_dir(origin_dir)
    target_dir = os.path.join(parent_dir,"new_images")
    create_new_empty_dir(target_dir)
    for image_path in file_list:
        new_image = regulize_image(image_path,300)
        _,file_name = get_parent_dir(image_path)
        cv2.imwrite(os.path.join(target_dir,file_name),new_image)
    return target_dir