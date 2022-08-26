import argparse
import os

import albumentations as A

from utils import *

category_ids = [0, 1, 2, 3]

augsuffixdict = {
    "clahe": "_CLAHE",
    "hflip": "_HFlip",
    "sunflare": "_SunFlare",
    "rndshadow": "_RNDShadow",
    "rndbrtcst": "_RNDBrightnessContrast"
}


def augmenter(augtype, trs):
    if augtype == "clahe":
        trs = A.Compose([A.CLAHE(p=1, always_apply=True)], bbox_params=A.BboxParams(format='yolo'))
    elif augtype == "hflip":
        trs = A.Compose([A.HorizontalFlip(p=1)], bbox_params=A.BboxParams(format='yolo'))
    elif augtype == "sunflare":
        trs = A.Compose(
            [A.RandomSunFlare(flare_roi=(0, 0, 1, 0.5), angle_lower=0, angle_upper=1, num_flare_circles_lower=6,
                              num_flare_circles_upper=10, src_radius=250, src_color=(255, 255, 255),
                              always_apply=True, p=1)], bbox_params=A.BboxParams(format='yolo'))
    elif augtype == "rndshadow":
        trs = A.Compose([A.RandomShadow(shadow_roi=(0, 0.5, 1, 1), num_shadows_lower=1,
                                        num_shadows_upper=2, shadow_dimension=5, always_apply=True, p=1)]
                        , bbox_params=A.BboxParams(format='yolo'))
    elif augtype == "rndbrtcst":
        trs = A.Compose([A.RandomBrightnessContrast(always_apply=True, p=1)], bbox_params=A.BboxParams(format='yolo'))
    return trs


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inpth', type=str, help='Input images directory path')
    parser.add_argument('--outpth', type=str, help='Output dataset path')
    parser.add_argument('--augtype', type=str, help='Augmentation type path')
    opt = parser.parse_args()
    return opt


def cordinates_to_list(list_crd):
    crd_list = []
    for crd in list_crd:
        temp_list = [float(i) for i in crd.albu_yolo().split(' ')]
        temp_list[-1] = int(temp_list[-1])
        crd_list.append(temp_list)
    return crd_list


def conv_to_yolo(list_crd):
    crd = []
    for crd in list_crd:
        temp_list = []
        temp_list[0] = int(crd[-1])
        temp_list[1:3] = crd[0:2]
        crd.append(temp_list)
    return crd


def name_generator(img_path, out_path, suffix):
    img_name = Path(img_path).stem
    out_path = str(Path(out_path))
    lbl_name = out_path + "/labels/" + img_name + suffix + ".txt"
    img_name = out_path + "/images/" + img_name + suffix + ".jpg"
    return img_name, lbl_name


def create_labels(cords_list, label_file_name):
    with open(label_file_name, "w+") as file:
        for cord in cords_list:
            st = str(cord[-1]) + " " + str(cord[0]) + " " + str(cord[1]) + " " + str(cord[2]) + " " + str(cord[3])
            file.write(st + "\n")


def check_path(pth):
    if not os.path.exists(pth):
        os.makedirs(pth)


def iter_over_imgs(in_path, out_path, aug_type):
    directory = in_path
    files = list(Path(directory).glob("*"))
    files_size = len(files)
    for file in tqdm(files, total=files_size):
        file_name = file.stem
        img = cv2.imread(str(file))
        lbl_pth = convert_imgpth_lblpth(file)
        check_path(lbl_pth)
        list_cords = list_label_cordinates(lbl_pth)
        crd_lst = cordinates_to_list(list_cords)
        try:
            transformed = transform(image=img, bboxes=crd_lst)
            f_name, lbl_name = name_generator(file, out_path, aug_type)
            create_labels(transformed['bboxes'], lbl_name)
            cv2.imwrite(f"{f_name}", transformed['image'])
        except:
            print("\nerror\n")


if __name__ == "__main__":
    opt = parse_opt()
    input_path = rf"{opt.inpth}"
    output_path = rf"{opt.outpth}"
    augtype = rf"{opt.augtype}"
    suffix = augsuffixdict[augtype]
    transform = None
    transform = augmenter(augtype, transform)
    check_path(f"{output_path}/labels")
    check_path(f"{output_path}/images")
    iter_over_imgs(input_path, output_path, suffix)
