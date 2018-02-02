import unittest
from sys import argv
import sqlite3

import wallet
from pycoin.tx.Tx import Tx, TxIn, TxOut
from pycoin.ui import standard_tx_out_script

TEST_EMAIL = 'jmdelaney8@gmail.com'
TEST_EMAIL_REC = 'deljm@umich.edu'
TEST_WALLET_KEY = 'xprv9s21ZrQH143K2cZXLUxwnVuc1Yt5uXEXGqP1xbei7rXEooe26rcf91gC7yMhFfGuBXHu5rwoXtf69fd2GCPHNY6cE5MFcbVAizwQ2vxoNDx'

if len(argv) > 1:
    SEND_EMAILS = argv[1] == 'send_emails'
else:
    SEND_EMAILS = False
    
class WalletTests(unittest.TestCase):
    def test_get_test_wallet_key_by_email(self):
        test_email = TEST_EMAIL
        test_wallet_key = TEST_WALLET_KEY
        self.assertEqual(test_wallet_key, wallet.get_wallet_key_by_email(test_email))

    def test_unknown_email(self):
        old_email = TEST_EMAIL
        new_email = TEST_EMAIL_REC
        self.assertTrue(wallet.unknown_email(new_email))
        self.assertFalse(wallet.unknown_email(old_email), "{} is an unknown email".format(old_email))
        
    def test_send_email_to_new_user(self):
        email = TEST_EMAIL_REC
        if SEND_EMAILS:
            wallet.send_email_to_new_user(email)

    def test_create_wallet_for_new_user(self):
        wallet.create_new_user_and_wallet(TEST_EMAIL_REC)
        self.assertFalse(wallet.unknown_email(TEST_EMAIL_REC))
    """
    def test_coinbase_tx_to_test_address(self):
        address 
        tx_in = TxIn.coinbase_tx_in(script=b'')
        tx_out = TxOut(50*1e8, standard_tx_out_script(address))
    """    


if __name__ == '__main__':
    unittest.main()
