"""Account object and functions useful for creating and managing an account"""

# fixme: move create_wallet to Wallet?

from pycoin.key.BIP32Node import BIP32Node
from pycoin.cmds import ku

from smtplib import SMTP_SSL
import sqlite3

# FIX ME -- there is probably a much better way to do this
WALLET_KEYS = 'var/wallet_keys.sqlite3'


def set_wallet_keys_location(file_path):
    """Sets the wallet_keys database to file_path given"""
    global WALLET_KEYS
    WALLET_KEYS = file_path


# REQUIRES: email be in wallet_keys database
# EFFECTS: returns a list of wallet keys associated with the given email
def get_wallet_keys_by_email(email):
    """
    Get account from wallet_keys database.
    Return all wallet_keys associated with account.
    """
    conn = sqlite3.connect(WALLET_KEYS)
    c = conn.cursor()
    query = (email, )
    c.execute('SELECT wallet_key FROM wallet_keys WHERE email=?', query)
    results = c.fetchall()
    wallet_keys = []
    for result in results:
        if result:
            wallet_keys.append(result[0])
    conn.close()
    return wallet_keys
    # return """xprv9s21ZrQH143K2cZXLUxwnVuc1Yt5uXEXGqP1xbei7rXEooe26rcf9
    #         1gC7yMhFfGuBXHu5rwoXtf69fd2GCPHNY6cE5MFcbVAizwQ2vxoNDx"""


# returns true if the email is not in the database, else false
def unknown_email(email):
    """If email in wallet_keys database, return true."""
    conn = sqlite3.connect(WALLET_KEYS)
    c = conn.cursor()
    query = (email, )
    c.execute('SELECT email FROM wallet_keys WHERE email=?', query)
    # print("output: ",c.fetchall())
    known_emails = c.fetchall()
    conn.close()
    if known_emails == []:
        return True
    return False


# REQUIRES: email not be an email already in the database
# EFFECTS: sends the standard new user email to email
def send_email_to_new_user(email):
    """Send the standard new user email to new user."""
    system_email = 'jmdelaney8@gmail.com'
    standard_msg = """Hello, you have received money.
                   You can retrieve it at my website"""
    server = SMTP_SSL("smtp.gmail.com", 465)
    server.login(system_email, "klcfkamvubxpcqit")
    server.sendmail(system_email, email, standard_msg)
    server.quit()


def add_wallet_key_to_account(email, wallet_key):
    """Update wallet_keys database adding wallet_key to account."""
    # fixme
    # assert wallet not already in account
    conn = sqlite3.connect(WALLET_KEYS)
    c = conn.cursor()
    query = [(wallet_key, email), ]
    c.executemany("""INSERT INTO wallet_keys(wallet_key, email)
                  VALUES (?,?)""", query)
    conn.commit()
    assert not unknown_email(email), """email and wallet key
               were not added to database"""
    conn.close()


# EFFECTS: Creates a new **PRIVATE** wallet key and returns key
def create_wallet_key():
    """Return new wallet_key based on os entropy"""
    wallet = BIP32Node.from_master_secret(ku.get_entropy())
    wallet_key = wallet.hwif(as_private=True)
    return wallet_key


# REQUIRES: email be in database
# MODIFIES: wallet_keys database
# EFFECTS: removes all the wallets from the database associated with email
def delete_all_account_wallets(email):
    """Delete all wallets associated with email"""
    conn = sqlite3.connect(WALLET_KEYS)
    c = conn.cursor()
    query = (email,)
    assert not unknown_email(email)
    c.execute('DELETE FROM wallet_keys WHERE email=?', query)
    conn.commit()
    assert unknown_email(email)
    conn.close()


# REQUIRES: email not already in wallet_keys.sqlite3
# MODIFIES: wallet_keys.sqlite3
# EFFECTS: adds email to database with a new wallet_key
def create_new_account_wallet(email):
    """Add a new wallet to account"""
    assert(unknown_email(email))
    wallet_key = create_wallet_key()
    add_wallet_key_to_account(email, wallet_key)


# REQUIRES: email in wallet_keys.sqlite3
# MODIFIES: wallet_keys.sqlite3
# EFFECTS: creates a new wallet and adds the key to the
#          users account. Returns the wallet key
def new_wallet_for_account(email):
    """Copy of create_new_account_wallet"""
    assert(not unknown_email(email))
    wallet_key = create_wallet_key()
    add_wallet_key_to_account(email, wallet_key)
    return wallet_key


# REQUIRES: email corresponds to an account
# EFFECTS: Returns true if account of email owns a wallet with key wallet_key
def account_contains_wallet(email, wallet_key):
    """Return true if wallet_key belongs to account of email."""
    conn = sqlite3.connect(WALLET_KEYS)
    c = conn.cursor()
    query = (email, )
    c.execute('SELECT wallet_key from wallet_keys where email= ?', query)
    results = c.fetchall()
    wallet_keys = []
    for result in results:
        wallet_keys.append(result[0])
    return wallet_key in wallet_keys


# REQUIRES: wallet_key be associated with the account owned by email.
#           email is a known account
# MODIFIES: wallet_keys
# EFFECTS: Removes wallet_key from account associated with email
def remove_wallet(email, wallet_key):
    """Remove wallet_key from account associated with email."""
    conn = sqlite3.connect(WALLET_KEYS)
    c = conn.cursor()
    query = (wallet_key,)
    assert account_contains_wallet(email, wallet_key)
    c.execute('DELETE FROM wallet_keys WHERE wallet_key=?', query)
    conn.commit()
    conn.close()
