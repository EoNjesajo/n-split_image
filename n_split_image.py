import os
import cv2
import random
import math
import shutil
from tqdm import tqdm
import albumentations as A

def __split__(images, labels, n) :
    data_list = []
    number, height, width, channel = image.shape
    for _ in range(4**n) :
        index = torch.randperm(images.size()[0]).cuda()
        split_image = images[index]
        split_label = labels[index]

        size_h = int(height/(2**n))
        size_w = int(width/(2**n))

        resize_trigger = random.randint(0,1)
        if resize_trigger == 0 :
            pass
        elif resize_trigger == 1 : #size up
            width = random.randint(int(width/(2**n)),width*2)
            height = random.randint(int(height/(2**n)),height*2)
            split_image = cv2.resize(split_image, dsize=(width, height), interpolation=cv2.INTER_LINEAR)
            split_label = cv2.resize(split_label, dsize=(width, height), interpolation=cv2.INTER_LINEAR)

        y = random.randint(0, height-size_h)
        x = random.randint(0, width-size_w)
        split_image = split_image[y:y+size_h, x:x+size_w]
        split_label = split_label[y:y+size_h, x:x+size_w]

        data_list.append({'img' : split_image, 'lab' : split_label})
    return data_list

def __paste__(raw,split) :
    img1 = cv2.hconcat([raw.pop(),raw.pop()])
    img2 = cv2.hconcat([raw.pop(),raw.pop()])
    grid = cv2.vconcat([img1,img2])
    split.append(grid)
    if len(raw) == 0 :
        if len(split) == 1 :
            return
        else :
            raw = split.copy()
            split.clear()
            __paste__(raw, split)
    else :
        __paste__(raw,split)

def __grid__(data_list, save_dir):
    split_img = []
    split_lab = []
    cache_images = []
    cache_labels = []
    for j in data_list :
        cache_images.append(j['img'])
        cache_labels.append(j['lab'])

    __paste__(cache_images, split_img)
    __paste__(cache_labels, split_lab)

    return split_img.pop(), split_lab.pop()

def split_image(images, labels) :
    n = random.randint(1,3)
    data_list = __split__(images, labels, n)
    split_img, split_lab =__grid__(data_list)
    
    return split_img, split_lab

split_image(images, labels)

