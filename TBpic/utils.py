from PIL import Image,ImageDraw,ImageFont
def load_images(file_list):
    imgs = []
    for path in file_list:
        img =Image.open(path)
        imgs.append(img)
    return imgs

def image_stitch(image1,image2,direction='bottom'):
    #将image2接在image1上，image2的尺寸会根据image1进行动态调整
    if direction=='bottom':
        new_w = image1.width
        new_h = int((new_w/image2.width)*image2.height)
        new_img = image2.resize(size=(new_w,new_h))

        score = Image.new('RGB', size=(image1.width, int(image1.height + new_h)))
        score.paste(image1)
        score.paste(new_img, box=(0, image1.height))

        return score

# 在图片的中间加一行字
# eg：score_bottom = add_text(score_bottom,'全谱共9页','汉仪小麦体简.ttf')

def add_text(image,text,font_file):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_file,size=100)
    txt = text
    font_size = font.getsize(text=txt)
    font_offset = font.getoffset(text=txt)
    # print(font_size,font_offset)
    t_x = int((image.width - font_size[0])/2)
    t_y = int((image.height-font_size[1])/2-font_offset[1])
    draw.text(xy=(t_x,t_y),text=txt,fill=(0),font=font)
    return image