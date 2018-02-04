from pycoin.key.BIP32Node import BIP32Node
from pycoin.cmds import ku

from smtplib import SMTP_SSL
import sqlite3

DB = 'var/wallet_keys.sqlite3'

def get_wallet_key_by_email(email):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    query = (email, )
    wallet_keys = c.execute('SELECT wallet_key FROM wallet_keys WHERE email=?', query)
    wallet_key = wallet_keys.fetchone()[0]
    conn.close()
    return wallet_key
    #return 'xprv9s21ZrQH143K2cZXLUxwnVuc1Yt5uXEXGqP1xbei7rXEooe26rcf91gC7yMhFfGuBXHu5rwoXtf69fd2GCPHNY6cE5MFcbVAizwQ2vxoNDx'

#returns true if the email is not in the database, else false
def unknown_email(email):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    query = (email, )
    c.execute('SELECT email FROM wallet_keys WHERE email=?', query)
    #print("output: ",c.fetchall())
    known_emails = c.fetchall()
    conn.close()
    if known_emails == []:
        return True
    return False

#REQUIRES: email not be an email already in the database
#sends the standard new user email to email
def send_email_to_new_user(email):
    system_email = 'jmdelaney8@gmail.com'
    standard_msg = "Hello, you have received money. You can retrieve it at my website"
    server = SMTP_SSL("smtp.gmail.com", 465)
    server.login(system_email, "klcfkamvubxpcqit")
    server.sendmail(system_email,email, standard_msg)
    server.quit()
    
#REQUIRES: email is not already in the database
#MODIFIES: adds entry to wallet_key datanase
#EFFECTS:  Creates new database entry (wallet key, email) and returns the wallet_key
def create_new_user_and_wallet(email):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    wallet_key = create_wallet_key().hwif(as_private=True)
    query = [(wallet_key, email),]
    assert(unknown_email(email))
    c.executemany('INSERT INTO wallet_keys(wallet_key, email) VALUES (?,?)', query)
    conn.commit()
    assert not unknown_email(email), "email and wallet key were not added to database"
    conn.close()
    return wallet_key

#EFFECTS: Creates a new **PRIVATE** wallet key and returns key object
def create_wallet_key():
    wallet = BIP32Node.from_master_secret(ku.get_entropy())
    return wallet

#REQUIRES: email be in database
#MODIFIES: wallet_keys database
#EFFECTS: removes all the wallets from the database associated with email
def delete_user_wallets(email):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    query = (email,)
    assert(not unknown_email(email))
    c.execute('DELETE FROM wallet_keys WHERE email=?', query)
    conn.commit()
    assert(unknown_email(email))
    conn.close()
