import unittest
from sys import argv,intern
import sqlite3
from pathlib import Path
import os

import wallet
from pycoin.tx.Tx import Tx, TxIn, TxOut
from pycoin.ui import standard_tx_out_script

TEST_WALLET_KEYS_PATH = 'var/test_wallet_keys.sqlite3'
TEST_EMAIL = 'jmdelaney8@gmail.com'
TEST_EMAIL_REC = 'deljm@umich.edu'
TEST_WALLET_KEY = 'xprv9s21ZrQH143K2cZXLUxwnVuc1Yt5uXEXGqP1xbei7rXEooe26rcf91gC7yMhFfGuBXHu5rwoXtf69fd2GCPHNY6cE5MFcbVAizwQ2vxoNDx'

if len(argv) > 1:
    SEND_EMAILS = argv[1] == 'send_emails'
else:
    SEND_EMAILS = False
    
class WalletTests(unittest.TestCase):
    def setUp(self):
        path = TEST_WALLET_KEYS_PATH
        #create test wallet_keys database from scratch
        p = Path(path)
        p.touch()
        conn = sqlite3.connect(path)
        wallet.set_wallet_keys_location(path)
        c = conn.cursor()
        c.execute('CREATE TABLE wallet_keys(wallet_key VARCHAR(111) NOT NULL, email VARCHAR(40) NOT NULL,PRIMARY KEY(wallet_key))')
        c.execute("""INSERT INTO wallet_keys(wallet_key, email)""" + 
                  """VALUES ('xprv9s21ZrQH143K2cZXLUxwnVuc1Yt5uXEXGqP1xbei7rXEooe26rcf91gC7yMhFfGuBXHu5rwoXtf69fd2GCPNY6cE5MFcbVAizwQ2vxoNDx', """+
                   """'jmdelaney8@gmail.com')""")
        conn.commit()
        conn.close()

    #TODO:
    #  make this test work when account(email) has more than one wallet associated with it
    def test_get_wallets_key_by_email(self):
        test_email = TEST_EMAIL
        test_wallet_key = TEST_WALLET_KEY
        print(test_wallet_key)
        print(wallet.get_wallet_keys_by_email(test_email)[0])
        #new_key = wallet.create_wallet_key()
        #self.assertFalse(intern(new_key) is intern(wallet.gets_wallet_key_by_email(test_email)))
        self.assertEqual(test_wallet_key, wallet.get_wallet_keys_by_email(test_email))

    def test_unknown_email(self):
        old_email = TEST_EMAIL
        new_email = TEST_EMAIL_REC
        self.assertTrue(wallet.unknown_email(new_email))
        self.assertFalse(wallet.unknown_email(old_email), "{} is an unknown email".format(old_email))
        
    def test_send_email_to_new_user(self):
        email = TEST_EMAIL_REC
        if SEND_EMAILS:
            wallet.send_email_to_new_user(email)

    def test_create_wallet_key(self):
        self.assertEqual(len(wallet.create_wallet_key()), 111)

    def test_create_wallet_for_new_account_and_delete_account_wallets(self):
        wallet.create_new_account_wallet(TEST_EMAIL_REC)
        self.assertFalse(wallet.unknown_email(TEST_EMAIL_REC))
        wallet.delete_all_account_wallets('deljm@umich.edu')
        self.assertTrue(wallet.unknown_email(TEST_EMAIL_REC))

    def test_existing_account_contains_wallet(self):
        email = TEST_EMAIL
        self.assertFalse(wallet.unknown_email(email))
        wallet_key = TEST_WALLET_KEY
        self.assertTrue(wallet.account_contains_wallet(email, wallet_key))
        
    def test_create_new_wallet_for_existing_user_and_delete_wallet(self):
        email = TEST_EMAIL
        self.assertFalse(wallet.unknown_email(email))
        new_wallet = wallet.new_wallet_for_account(TEST_EMAIL)
        #TODO
        #wallets = #add new_wallet to wallets
    
        
        
        
        
        
    #"""
    #def test_coinbase_tx_to_test_address(self):
    #    address 
    #    tx_in = TxIn.coinbase_tx_in(script=b'')
    #    tx_out = TxOut(50*1e8, standard_tx_out_script(address))
    #"""    

    def tearDown(self):
        conn = sqlite3.connect(TEST_WALLET_KEYS_PATH)
        c = conn.cursor()
        c.execute('DROP TABLE wallet_keys')
        conn.commit()
        conn.close()
        os.remove('var/test_wallet_keys.sqlite3')
        
if __name__ == '__main__':
    unittest.main()
