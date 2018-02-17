"""
wallet index (main) view.

URLs include:
/
"""
import flask
from flask import request, redirect, url_for, render_template
import wallet
from Account import known_email, Account

@wallet.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    context = {}
    if request.method == 'POST' and login(request.form['email']):
        return redirect(url_for('homepage', email=request.form['email']))
    return render_template("index.html", **context)

    
def login(email):
    """
    Check user identification and return True if user passes login.
    """
    # FIXME actually check login
    if known_email(email):
        session['email'] = email
        account = Account(email)
        return True 
    return False

@wallet.app.route('/u/', methods=['GET', 'POST'])
@wallet.app.route('/u/<email>', methods=['GET', 'POST'])
def homepage(email=None):
    return render_template("homepage.html", email=email)


# FIXME: this should probably be made more secure
# should I switch to server-side session handling?
wallet.app.secret_key = '\xa1\x91\x8b\xd6Bz\x82\x89\x85\x16\xdfRY\xa1\xad\xdb\xe0\xbb\xdb\x8e\x9cI\xd4\xaf'






