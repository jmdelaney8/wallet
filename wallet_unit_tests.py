import unittest
from sys import argv,intern
import sqlite3
from pathlib import Path
import os

import Account
from pycoin.key.BIP32Node import BIP32Node

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
        Account.set_wallet_keys_location(path)
        c = conn.cursor()
        c.execute('CREATE TABLE wallet_keys(accountID INTEGER PRIMARY KEY, wallet_key BLOB(111), email VARCHAR(40) NOT NULL)')
        c.execute("""INSERT INTO wallet_keys(wallet_key, email)""" + 
                  """VALUES ('xprv9s21ZrQH143K2cZXLUxwnVuc1Yt5uXEXGqP1xbei7rXEooe26rcf91gC7yMhFfGuBXHu5rwoXtf69fd2GCPHNY6cE5MFcbVAizwQ2vxoNDx', """+
                   """'jmdelaney8@gmail.com')""")
        conn.commit()
        conn.close()

    #TODO:
    #  make this test work when account(email) has more than one wallet associated with it
    def test_get_wallets_key_by_email(self):
        test_email = TEST_EMAIL
        test_wallet_key = TEST_WALLET_KEY
        account = Account.Account(test_email)
        self.assertTrue(test_wallet_key in account.get_wallet_keys())

    def test_known_email(self):
        old_email = TEST_EMAIL
        new_email = TEST_EMAIL_REC
        self.assertTrue(Account.known_email(old_email))
        self.assertFalse(Account.known_email(new_email), "{} is an known email".format(new_email))

  
   #def test_unknown_email(self):
   #     old_email = TEST_EMAIL
   #     new_email = TEST_EMAIL_REC
   #     self.assertTrue(wallet.unknown_email(new_email))
   #     self.assertFalse(wallet.unknown_email(old_email), "{} is an unknown email".format(old_email))
        
    def test_send_email_to_new_user(self):
        email = TEST_EMAIL_REC
        if SEND_EMAILS:
            account = Account.Account(email)
            account.send_new_account_email()

    def test_create_wallet_key(self):
        account = Account.Account(TEST_EMAIL)
        self.assertEqual(len(account.new_wallet_key()), 111)

    def test_create_wallet_for_new_account_and_delete_account_wallets(self):
        account = Account.Account(TEST_EMAIL_REC)
        self.assertTrue(Account.known_email(TEST_EMAIL_REC))
        account.delete_account()
        self.assertFalse(Account.known_email(TEST_EMAIL_REC))

    def test_existing_account_contains_wallet(self):
        email = TEST_EMAIL
        account = Account.Account(email)
        self.assertTrue(Account.known_email(email))
        wallet_key = TEST_WALLET_KEY
        self.assertTrue(account.contains_wallet(wallet_key))
        new_key = Account.create_wallet_key()
        self.assertFalse(account.contains_wallet(new_key))
        
    def test_create_new_wallet_for_existing_account_and_delete_wallet(self):
        email = TEST_EMAIL
        self.assertTrue(Account.known_email(email))
        account = Account.Account(email)
        new_wallet = account.new_wallet_key()
        self.assertTrue(account.contains_wallet(new_wallet))
        account.remove_wallet(new_wallet)
        self.assertFalse(account.contains_wallet(new_wallet))

    def test_import_wallet_for_new_account(self):
        import_key_ = Account.create_wallet_key()
        account = Account.Account(TEST_EMAIL_REC, import_key = import_key_)
        self.assertTrue(account.contains_wallet(import_key_))

    def test_derive_child_from_wallet_key(self):
        account = Account.Account(TEST_EMAIL)
        wallet = BIP32Node.from_wallet_key(account.get_wallet_keys()[0])
        print(wallet.subkey())
        
        
        
        
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
