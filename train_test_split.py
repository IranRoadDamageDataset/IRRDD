import argparse
import os
import random
import shutil


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--split',default=0.2, type=float, help='Enter Split value')
    opt = parser.parse_args()
    return opt


def check_path(pth):
    if not os.path.exists(pth):
        os.makedirs(pth)

if __name__ == '__main__':
    opt = parse_opt()
    imgList = os.listdir('images')
    random.shuffle(imgList)
    split = opt.split
    print(f"Split ratio = {split}")
    train_path_img = 'IRRDD/train/images'
    train_path_lbl = 'IRRDD/train/labels'
    val_path_img = 'IRRDD/val/images'
    val_path_lbl = 'IRRDD/val/labels'
    check_path(train_path_img)
    check_path(train_path_lbl)
    check_path(val_path_img)
    check_path(val_path_lbl)
    imgLen = len(imgList)
    print("Images in total: ", imgLen)
    train_images = imgList[: int(imgLen - (imgLen * split))]
    val_images = imgList[int(imgLen - (imgLen * split)):]
    print("Training images: ", len(train_images))
    print("Validation images: ", len(val_images))

    for imgName in train_images:
        og_path = os.path.join('images', imgName)
        target_path = os.path.join(train_path_img, imgName)
        shutil.copyfile(og_path, target_path)
        og_txt_path = os.path.join('labels', imgName.replace('.jpg', '.txt'))
        target_txt_path = os.path.join(train_path_lbl, imgName.replace('.jpg', '.txt'))
        shutil.copyfile(og_txt_path, target_txt_path)

    for imgName in val_images:
        og_path = os.path.join('images', imgName)
        target_path = os.path.join(val_path_img, imgName)
        shutil.copyfile(og_path, target_path)
        og_txt_path = os.path.join('labels', imgName.replace('.jpg', '.txt'))
        target_txt_path = os.path.join(val_path_lbl, imgName.replace('.jpg', '.txt'))
        shutil.copyfile(og_txt_path, target_txt_path)

    print("Done! ")
