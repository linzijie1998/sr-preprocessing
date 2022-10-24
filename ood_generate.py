# -*- coding: utf-8 -*-
import os
import argparse

from glob import glob
from PIL import Image


def ood_images(path, dataset, upscale):
    output_path = os.path.join(path, dataset, f"image_SRF_{upscale}")
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    hr_path = sorted(glob(os.path.join(path, dataset, "image_SRF_2", "*_HR.png")))
    print(hr_path)
    for i, path in enumerate(hr_path):
        img = Image.open(path)
        # make img shape divisible by the scale
        w = img.width // upscale * upscale
        h = img.height // upscale * upscale
        cropped_img = img.crop((0, 0, w, h))
        resized_img = cropped_img.resize((w // upscale, h // upscale), resample=Image.Resampling.BICUBIC, box=None, reducing_gap=None)
        # resized_img = resized_img.resize((w, h), resample=Image.Resampling.BICUBIC, box=None, reducing_gap=None)
        cropped_img.save(os.path.join(output_path, f"img_{str(i + 1).zfill(3)}_SRF_{upscale}_HR.png"))
        resized_img.save(os.path.join(output_path, f"img_{str(i + 1).zfill(3)}_SRF_{upscale}_LR.png"))


def main():
    parser = argparse.ArgumentParser(description="ood generate")
    parser.add_argument("--path", type=str, default="images")
    parser.add_argument("--dataset", type=str, default="Set5")
    parser.add_argument("--upscale", type=int, default=6)
    args = parser.parse_args()
    print(args)
    ood_images("./images", "Set5", 12)


if __name__ == '__main__':
    main()
