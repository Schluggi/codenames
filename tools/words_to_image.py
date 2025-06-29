#!/usr/bin/env python3
import os.path
from os import listdir, mkdir
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DIR_WORDS = 'words/'
DIR_OUTPUT = '../codenames/static/img/codes/classic/'
W_IMG = 950
H_IMG = 950
FONT_TYPE = 'LiberationSans-Bold.ttf'
FONT_SIZE = 100

path = Path(__file__).parent.absolute()
font = ImageFont.truetype(os.path.join(path, FONT_TYPE), FONT_SIZE)

for filename in [f for f in listdir(os.path.join(path, DIR_WORDS)) if f.endswith('.txt')]:
    print(f'Progressing "{filename}"')
    lang = filename.rsplit('.txt', 1)[0].lower()
    with open(os.path.join(path, DIR_WORDS, filename), encoding="utf-8") as lf:
        for code in [line for line in lf.read().split('\n') if line]:
            code = code.upper()

            img = Image.new('RGB', (W_IMG, H_IMG), color=(255, 245, 234))
            draw = ImageDraw.Draw(img)

            w_text = draw.textlength(code, font=font)
            draw.text(((W_IMG - w_text) / 2, (H_IMG - FONT_SIZE) / 2), code, font=font, fill="black")

            dir_lang = os.path.join(path, DIR_OUTPUT, lang)

            if os.path.isdir(dir_lang) is False:
                mkdir(dir_lang)

            img.save(os.path.join(dir_lang, f'{lang}_{code.lower()}.webp'), quality=75)
