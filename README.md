# Codenames

<a href="https://www.buymeacoffee.com/schluggi" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

I like the game cardboard game [codenames](https://en.wikipedia.org/wiki/Codenames_\(board_game\)) and now that COVID-19
is part of our life I have played a lot online with my friends on [this](https://www.horsepaste.com/) website. But I
realized that I want to play codename pictures instead. So I've decided to create my own.

# Features

- Realtime online multiplayer
- Multiple game modes:
    - Codename classic (multiple languages)
    - Codename pictures
- Add your own images/words if you want to
- Just like the codenames board game but online

# Quickstart

## Docker

```commandline
docker run -p 5000:5000 -e GAME_MODES="pictures,classic_de,classic_en,classic_en-undercover" <placeholder>:latest 
```

## Git

```commandline
git clone git@github.com:Schluggi/codenames.git
cd codenames
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 tools/words_to_image.py
flask --app codenames run
```

# Configuring

## Environment variables

### Main Game

| name       | Description                                    | required | default                                              |
|------------|------------------------------------------------|----------|------------------------------------------------------|
| GAME_MODES | A comma separated list of available game modes | No       | pictures,classic_de,classic_en,classic_en-undercover |
| SECRET_KEY | A secret key to encrypt the user sessions      | No       | \<a random key will be created\>                     |

### Tools (optional)

| name             | Description           | required | default |
|------------------|-----------------------|----------|---------|
| OPENAI_API_TOKEN | Your OPENAI API token | Yes      | -       |

## Create a new image
> If you already had images you want to import see [Import images](#import-images)

First you need an OpenAI API token. You can get one [here](https://platform.openai.com/). Make sure you have access to the `gpt-image-1` model.
To generate a new image you can use the script `tools/create_new_image.py`. Just execute and input your prompt. Do not include colors or styling in your prompt.
This is handled by the script. The script also unionize the background color and saves the images as a webp-file. Done.

## Add new words or languages

In this example we'll add france as language for the classic mode.

1. Create a language file: `tools/words/fr.txt` (one word each line)
2. Run the script (existing files will be overwritten)
    ```commandline
    python3 tools/words_to_image.py
    ```
3. Append `classic_fr` to your `GAME_MODES` environment variable

## Import images

To get the best experience it's recommend to buy the original cardboard game and scan all images. In my case I scanned
all pictures with 400dpi and used [picpunch](https://github.com/Schluggi/picpunch) to cut them to size and render for
web (`--border 5 --quallity 30`).The new images have to be placed into the corresponding folders.

The code images into (at least 20):

- `codenames/static/images/codes`

And the colored team cards (at least 1 each):

- `codenames/static/images/cards/assassin`
- `codenames/static/images/cards/blue`
- `codenames/static/images/cards/neutral`
- `codenames/static/images/cards/red`

The filename does not matter. But the file extension and type has to be JPEG/JPG, PNG or WEBP.

# Credits

Created and maintained by Schluggi.
