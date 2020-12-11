#!/usr/bin/python3
from os import listdir, mkdir
from os.path import join as pjoin, isdir
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

dir_words = './words/'
dir_output = '../codenames/static/img/codes/classic/'
w_img = 950
h_img = 950
font_type = 'LiberationSans-Bold.ttf'
font_size = 100

path = Path(__file__).parent.absolute()
font = ImageFont.truetype(font_type, font_size)

for filename in [f for f in listdir(pjoin(path, dir_words)) if f.endswith('.txt')]:
    print(f'Progressing "{filename}"')
    lang = filename.rsplit('.txt', 1)[0].lower()
    with open(pjoin(path, dir_words, filename)) as lf:
        for code in [line for line in lf.read().split('\n') if line]:
            code = code.upper()

            img = Image.new('RGB', (w_img, h_img), color=(255, 255, 221))
            draw = ImageDraw.Draw(img)

            w_text, h_text = draw.textsize(code, font=font)
            draw.text(((w_img-w_text)/2, (h_img-h_text)/2), code, font=font, fill="black")

            dir_lang = pjoin(path, dir_output, lang)

            if isdir(dir_lang) is False:
                mkdir(dir_lang)

            img.save(pjoin(dir_lang, f'{lang}_{code.lower()}.jpg'))
