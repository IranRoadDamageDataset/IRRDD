import glob
import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
import random
from tqdm import tqdm
import cv2
from PIL import Image


@dataclass
class RandBound:
    low: int
    high: int


@dataclass
class cordinates:
    cls_name: int
    x_pos: int
    y_pos: int
    width: int
    hight: int

    def yolo_str(self):
        string = (self.cls_name) + " " + (self.x_pos) + " " + (self.y_pos) + " " + (self.width) + " " + (self.hight)
        return string
    def albu_yolo(self):
        string =   (self.x_pos) + " " + (self.y_pos) + " " + (self.width) + " " + (self.hight) + " " + (self.cls_name)
        return string


def resize_dir(in_path, out_path, size_bound, desired_size):
    directory = in_path
    files = list(Path(directory).glob("*"))
    for file in tqdm(files, total=len(files)):
        img_resize_dir(file, out_path, size_bound, desired_size)


def resize_dir_random(in_path, out_path, w_bound, h_bound):
    directory = in_path
    files = list(Path(directory).glob("*"))
    for file in tqdm(files, total=len(files)):
        rand_bound_resize(file, out_path, w_bound, h_bound)


def resize_dir_fixed(in_path, out_path, width, height):
    directory = in_path
    files = list(Path(directory).glob("*"))
    for file in tqdm(files, total=len(files)):
        fix_image_resize(file, out_path, width, height)


def img_resize_dir(img_path, out_path, size_bound, desired_size):
    img_path = Path(img_path)
    out_path = Path(out_path)
    file_name = img_path.name
    img = cv2.imread(str(img_path))
    h = img.shape[0]
    w = img.shape[1]
    area = w * h
    aspect_ratio = w / h
    if area >= size_bound:
        h_new = int(float(math.sqrt(desired_size / aspect_ratio)))
        w_new = int(h_new * aspect_ratio)
        img2 = cv2.resize(img, (w_new, h_new), interpolation=cv2.INTER_AREA)
        try:
            cv2.imwrite(f"{out_path}/{file_name}", img2)
        except:
            print("error")
    else:
        shutil.copy(img_path, f"{out_path}/{file_name}")


def rand_bound_resize(img_path, out_path, w_bound, h_bound):
    height = random.randrange(w_bound.low, w_bound.high)
    width = random.randrange(h_bound.low, h_bound.high)
    img_path = Path(img_path)
    out_path = Path(out_path)
    file_name = img_path.name
    img = cv2.imread(str(img_path))
    img2 = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    try:
        cv2.imwrite(f"{out_path}/{file_name}", img2)
    except:
        print("error")


def fix_image_resize(img_path, out_path, width, height):
    img_path = Path(img_path)
    out_path = Path(out_path)
    file_name = img_path.name
    img = cv2.imread(str(img_path))
    img_size_target = width * height
    w1,h1 ,r1=  img.shape
    img_size1 = w1 * h1
    if img_size1 > img_size_target/3:
        img2 = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
        file_path = f"{out_path}/{file_name}"
        try:
            cv2.imwrite(file_path, img2)
        except:
            print("error")


def generate_file_name(pre_name, filepath, extention):
    filepath = Path(filepath)
    file_name = str(filepath.stem)
    file_name = pre_name + file_name + extention
    return file_name


def make_dir(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        file_path.mkdir(parents=True, exist_ok=True)


def convert_imgpth_lblpth(inpath):
    inpath = str(inpath).replace("images", "labels").replace(".jpg", ".txt")
    return inpath


def convert_lblpth_imgpth(inpath):
    inpath = str(inpath).replace("labels", "images").replace(".txt", ".jpg")
    return inpath


def list_label_cordinates(labelname_pth):
    with open(labelname_pth, "r+") as file:
        labels_lines = file.read().splitlines()
        list_labels = []
        for line in labels_lines:
            temp_lst = line.split()
            lbl_cor = cordinates(temp_lst[0], temp_lst[1], temp_lst[2], temp_lst[3], temp_lst[4])
            list_labels.append(lbl_cor)
        return list_labels


def paste_img(img_src_path, img2_path, x0y0, save_path):
    img1 = Image.open(img_src_path)
    img2 = Image.open(img2_path)
    Image1copy = img1.copy()
    Image1copy.paste(img2, x0y0)
    Image1copy.save(save_path)


def increment_path(path, exist_ok=False, sep='', mkdir=False):
    # Increment file or directory path, i.e. runs/exp --> runs/exp{sep}2, runs/exp{sep}3, ... etc.
    path = Path(path)  # os-agnostic
    if path.exists() and not exist_ok:
        path, suffix = (path.with_suffix(''), path.suffix) if path.is_file() else (path, '')
        dirs = glob.glob(f"{path}{sep}*")  # similar paths
        matches = [re.search(rf"%s{sep}(\d+)" % path.stem, d) for d in dirs]
        i = [int(m.groups()[0]) for m in matches if m]  # indices
        n = max(i) + 1 if i else 2  # increment number
        path = Path(f"{path}{sep}{n}{suffix}")  # increment path
    if mkdir:
        path.mkdir(parents=True, exist_ok=True)  # make directory
    return path
