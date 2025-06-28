#!/usr/bin/env python3
import base64
import io
import os
import uuid

import openai
from PIL import Image

openai.api_key = os.getenv('OPENAI_API_TOKEN')


def generate_image_from_text(prompt: str) -> Image:
    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        n=1,
        quality="high",
    )
    return Image.open(io.BytesIO(base64.b64decode(response.data[0].b64_json)))


def replace_background_color(img: Image, background_color: tuple[int, int, int], threshold: int = 10) -> Image:
    img = img.convert("RGBA")
    datas = img.getdata()

    current_background_color = datas[0]

    new_datas = []
    for item in datas:
        if all(abs(item[i] - current_background_color[i]) < threshold for i in range(3)):
            new_datas.append(background_color + (255,))
        else:
            new_datas.append(item)

    img.putdata(new_datas)
    return img


if __name__ == "__main__":
    user_prompt = input('Describe your image: ').strip()
    print('Generating image (this can take a while) ...')
    image = generate_image_from_text(
        f'{user_prompt}. The design is in a minimalist, retro-inspired vector style, with clean lines and simple grey colors on a light bisque background.')

    if image:
        image = replace_background_color(image, (255, 245, 234), threshold=10)

        IMAGE_NAME = f'{str(uuid.uuid4())}.webp'
        image_path = os.path.join('../codenames/static/img/codes/pictures/', IMAGE_NAME)
        image.save(image_path, quality=75)
        print(f'Image saved as {IMAGE_NAME}')
    else:
        print('error creating image')
