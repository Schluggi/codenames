#!/usr/bin/env python3
import base64
import io
import os
import uuid

import openai
from PIL import Image

openai.api_key = os.getenv('OPENAI_API_TOKEN')


def generate_image_from_text(prompt: str, n: int = 1) -> list:
    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        n=n,
        quality="high",
    )

    all_images = []

    for openai_img in response.data:
        all_images.append(Image.open(io.BytesIO(base64.b64decode(openai_img.b64_json))))

    return all_images


def replace_background_color(image: Image, background_color: tuple[int, int, int], threshold: int = 10) -> Image:
    image = image.convert("RGBA")
    data = image.getdata()

    current_background_color = data[0]

    new_data = []
    for item in data:
        if all(abs(item[i] - current_background_color[i]) < threshold for i in range(3)):
            new_data.append(background_color + (255,))
        else:
            new_data.append(item)

    image.putdata(new_data)
    return image


if __name__ == "__main__":
    user_prompt = input('Describe your image: ').strip()
    print('Generating image (this can take a while) ...')
    images = generate_image_from_text(
        f'{user_prompt}. The design is in a minimalist, retro-inspired vector style, with clean lines and simple grey colors on a light bisque background.')

    if images:
        for img in images:
            img = replace_background_color(img, (255, 245, 234), threshold=10)
            IMAGE_NAME = f'{str(uuid.uuid4())}.webp'
            image_path = os.path.join('../codenames/static/img/codes/pictures/', IMAGE_NAME)
            img.save(image_path, quality=75)
            print(f'Image saved as {IMAGE_NAME}')
    else:
        print('error creating image')
