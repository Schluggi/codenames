# Codenames
<a href="https://www.buymeacoffee.com/schluggi" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>


I like the game cardboard game [codenames](https://en.wikipedia.org/wiki/Codenames_\(board_game\)) and now that COVID-19 is
part of our life I have played a lot online with my friends on [this](https://www.horsepaste.com/) website. But I 
realized that I want to play codename pictures instead. So I've decided to create my own.

## Features
- Realtime online multiplayer
- Multiple game modes:
    - Codename classic (with words)
    - Codename pictures  
        - Does not include any images (for copyright reasons, but you can import your own)
- Just like the codenames board game...

## Requirements
- Python >= 3.6
- [Almost every](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls) database engine is supported (SQLite
 in memory by default)

## Installation & Quickstart
1. Clone this repo
2. Create a virtualenv and join them
3. Install python requirements
    ```shell script
    $ pip3 install -r requirements.txt   
    ```
4. Generate text images (for the classic mode) 
    ```shell script
    $ ./words2img/words2img.py
    ```
    Optional: [Import images](https://github.com/Schluggi/codenames#import-images) for picture mode
5. Configuration
    - 5.1 Create a secret key by running `python3 -c "import os; print(os.urandom(24).hex())"` and insert that key into the 
`config.py`
6. Test your setup by running `flask run`
7. If everything works as expected, you should now be able to play at `http://localhost:5000` 

## Configuring
### Add new words or languages
In this example we'll add france as language for the classic mode.

1. Create a language file: `./words2img/words/fr.txt` (one word each line)
2. Run the script (existing files will be overwritten)
    ```shell script
    $ python3 ./words2img/words2img.py
    ```
3. Append `classic_fr` to the `GAME_MODES` list in the `config.py`

### Import images
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

The filename does not matter. But the file extension and type has to be JPEG/JPG.

### Apache2 with mod_wsgi
`flask run` works fine but you should'nt use it for production deployment. However you can use Apache2 instead. 
If not already installed you have to install `libapache2-mod-wsgi-py3`. After installation you can create a virtualhost
like in this example:

```
<VirtualHost *:80>
        ServerName codenames.example.org
        Redirect / https://codenames.example.org/
</VirtualHost>

<VirtualHost *:443>
        ServerName codenames.example.org
        
        WSGIDaemonProcess wsgi_codenames user=www-data group=www-data processes=1 threads=5 python-home=python-home=/virtualenvs/codenames/
        WSGIScriptAlias / /var/www/codenames/wsgi.py

        SSLEngine On
        SSLCertificateFile /etc/letsencrypt/live/codenames.example.org/cert.pem
        SSLCertificateKeyFile /etc/letsencrypt/live/codenames.example.org/privkey.pem
        SSLCertificateChainFile /etc/letsencrypt/live/codenames.example.org/chain.pem
        SSLProtocol ALL -SSLv2 -SSLv3
        SSLHonorCipherOrder On
        SSLCipherSuite ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+3DES:DH+3DES:
        SSLCompression Off
        Header always set Strict-Transport-Security "max-age=63072000; includeSubdomains; preload"

        <Directory /var/www/codenames/>
                WSGIProcessGroup wsgi_codenames
                WSGIApplicationGroup %{GLOBAL}
        </Directory>
</VirtualHost>
```
I use Let's Encrypt for free ssl certificates. Please ensure that all paths are correct. After restating Apache2,
codenames should be run as part of the Apache2-daemon.

## Credits
Created and maintained by Schluggi.
