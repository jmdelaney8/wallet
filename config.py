"""
wallet development configuration
"""

import os

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATOIN_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'oeO\x0b!\xc4\xe7n]\xbaWL\xcc\x83!2\x1b\xb6\x1d)\xb0Zs\xdd'
# b'FIXME SET THIS WITH: $ python3.6 -c "import os;print(0s.urandom(24))" '
# nowa: E501 pylint: disable=line-too-long

SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
UPLOAD_FOLDER = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'uploads'
)
# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/wallet.sqlite3
DATABASE_FILENAME = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'var', 'wallet.sqlite3'
)
