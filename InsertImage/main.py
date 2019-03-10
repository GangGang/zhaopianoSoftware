import os
import shutil

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

def fixed_length(num,length):
    a = str(num)
    while len(a) < length:
        a = '0'+a
    return a
if __name__ == "__main__":
    img_folder = "/Users/shidanlifuhetian/Downloads/讲义"
    extra_img_path = "/Users/shidanlifuhetian/Desktop/淘宝违规清零规则.jpg"
    insert_pos = 70 # 新图像取代原第x张的位置。（真实的第x张，从1开始数）
    extention ="jpg"

    posA = 8
    posB = 69
    parent_dir,_ = get_parent_dir(img_folder)
    new_folder = os.path.join(parent_dir,"讲义new")
    create_new_empty_dir(new_folder)
    img_list = get_dir_filelist_by_extension(img_folder,extention)
    img_list.sort()

    shutil.copy(extra_img_path,os.path.join(new_folder,fixed_length(insert_pos,3)+"."+extention))
    for img_path in img_list:
        index = int(img_path.rsplit("/")[-1].split(".")[0])
        #
        # if 8<=index<=69:
        #     new_name = fixed_length(index - 1, 3)
        # else:
        #     new_name = fixed_length(index, 3)

        if index < insert_pos:
            new_name = fixed_length(index,3)
        elif index >= insert_pos:
            new_name = fixed_length(index+1,3)
        shutil.copy(img_path,os.path.join(new_folder,new_name+"."+extention))