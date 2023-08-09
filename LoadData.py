from PIL import Image
import numpy as np


def load_image(img_path):
    img_path = r'input/' + img_path
    img = Image.open(img_path)
    # print(type(img))
    img_arr = np.array(img)
    # height = img_arr.__len__()
    # width = img_arr[0].__len__()
    # channel = img_arr[0][0].__len__()
    # print(height, width, channel)
    return img_arr


def load_image_inv(img_path):
    img_path = r'output/' + img_path
    img = Image.open(img_path)
    img_arr = np.array(img)
    # print(img_arr)
    # height = img_arr.__len__()
    # width = img_arr[0].__len__()
    # channel = img_arr[0][0].__len__()
    # print(height, width, channel)
    return img_arr


def load_text(text_path):
    text_path = r'input/' + text_path
    with open(text_path, encoding='utf-8') as text_file:
        text = text_file.read()
    text_arr = []
    for ch in text:
        text_arr.append(ord(ch))
    # print(text_arr)
    return text_arr


def save_img(img_arr, img_path, is_jpg):
    img = Image.fromarray(img_arr)
    img_path = r'output/' + img_path
    if is_jpg:
        img.save(img_path, format="JPEG", quality=200)
    else:
        img.save(img_path)
