"""
SQLALCHEMY_DATABASE_URI
    Almost every database engine is supported.
    Check out this link for more information about database URLs:
        https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls

SECRET_KEY
    You can create a secret key by running:
        python3 -c "import os; print(os.urandom(24).hex())"

See https://github.com/Schluggi/codenames for more information.
"""

SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
SECRET_KEY = '<insert your key here>'
