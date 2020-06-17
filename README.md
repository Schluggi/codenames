# Codenames
[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=KPG2MY37LCC24&source=url)

I like the game [codenames](https://en.wikipedia.org/wiki/Codenames_(board_game)) and since COVID-19 is part of our life
i have played a lot online with my friends on [this](https://www.horsepaste.com/) website. But i realized that i want to
play codename pictures instead. So i've decided to create my own.

## Features
- Realtime only multiplayer 
- Does not include any original images (for copyright reasons, but you can import your own images)
- It's just codenames pictures...

## Requirements
- Python >= 3.7 (lower versions may also work)
- [Almost every](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls) database engine is supported (SQLite
 in memory by default)

## Installation & Quickstart
1. Clone this repo
2. Create an and join the virtualenv
3. Install python requirements
    ```shell script
    $ pip3 install -r requirements.txt   
    ```
4. Put at least 20 different code images into the image directory (`codenames/static/images/codes` by default)
5. Create a secret key by running `python3 -c "import os; print(os.urandom(24).hex())"` and insert that key into the 
`config.py` 
6. Test your setup by running `flask run`
7. If everything works as expected, you should now be able to play at `http://localhost:5000` 

## Configuring
### Apache2 with mod_wsgi
`flask run` works fine but you should'nt use it for production deployment. However you can use Apache2 instead. 
If not already installed you have to install `libapache2-mod-wsgi-py3`. After installation you can create a virtualhost
like in this example:

```
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
