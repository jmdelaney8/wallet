import unittest
from sys import argv,intern
import sqlite3
from pathlib import Path
import os

import Account
import Wallet
from pycoin.key.validate import is_address_valid
from pycoin.tx.Tx import Tx, TxIn, TxOut
from pycoin.ui import standard_tx_out_script

TEST_WALLET_KEYS_PATH = 'var/test_wallet_keys.sqlite3'
TEST_EMAIL1 = 'cryptowallettest1@gmail.com'
TEST_EMAIL2 = 'cryptowallettest2@gmail.com'
TEST_EMAIL3 = 'cryptowallettest3@aol.com'
TEST_WALLET_KEY1 = 'xprv9s21ZrQH143K2cZXLUxwnVuc1Yt5uXEXGqP1xbei7rXEooe26rcf91gC7yMhFfGuBXHu5rwoXtf69fd2GCPHNY6cE5MFcbVAizwQ2vxoNDx'
TEST_WALLET_KEY2 = 'xprv9s21ZrQH143K4KyJQSfVvjxgLbBQwZjmvZ9Srno2gLovYoJ7pAuLn48eAsobgzZdY8xtGPb9sVeXn7BCAgRfXoKpJiGsEw7w8AfAdkrb3MT'

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
        c.execute("INSERT INTO wallet_keys(wallet_key, email) VALUES ('xprv9s21ZrQH143K2cZXLUxwnVuc1Yt5uXEXGqP1xbei7rXEooe26rcf91gC7yMhFfGuBXHu5rwoXtf69fd2GCPHNY6cE5MFcbVAizwQ2vxoNDx', 'cryptowallettest1@gmail.com'), ('xprv9s21ZrQH143K4KyJQSfVvjxgLbBQwZjmvZ9Srno2gLovYoJ7pAuLn48eAsobgzZdY8xtGPb9sVeXn7BCAgRfXoKpJiGsEw7w8AfAdkrb3MT', 'crypwallettest2@gmail.com')")
        conn.commit()
        c.execute('CREATE TABLE utxos(txID INTEGER PRIMARY KEY, tx_hex BLOB(170) NOT NULL, email VARCHAR(48) NOT NULL)')
        c.execute("INSERT INTO utxos(tx_hex, email) VALUES ('01000000010000000000000000000000000000000000000000000000000000000000000000ffffffff00ffffffff0100f2052a010000001976a914396aa1dc70fe8f72119fbb714978255cb9f4d03d88ac00000000', 'cryptowallettest1@gmail.com')")
        conn.close()

    #TODO:
    #  make this test work when account(email) has more than one wallet associated with it
    def test_get_wallets_key_by_email(self):
        test_email = TEST_EMAIL1
        test_wallet_key = TEST_WALLET_KEY1
        account = Account.Account(test_email)
        self.assertTrue(test_wallet_key in account.get_wallet_keys())

    def test_known_email(self):
        old_email = TEST_EMAIL1
        new_email = TEST_EMAIL3
        self.assertTrue(Account.known_email(old_email))
        self.assertFalse(Account.known_email(new_email), "{} is an known email".format(new_email))

  
   #def test_unknown_email(self):
   #     old_email = TEST_EMAIL
   #     new_email = TEST_EMAIL_REC
   #     self.assertTrue(wallet.unknown_email(new_email))
   #     self.assertFalse(wallet.unknown_email(old_email), "{} is an unknown email".format(old_email))
        
    def test_send_email_to_new_user(self):
        email = TEST_EMAIL3
        if SEND_EMAILS:
            account = Account.Account(email)
            account.send_new_account_email()

    def test_create_wallet_key(self):
        account = Account.Account(TEST_EMAIL1)
        self.assertEqual(len(account.new_wallet_key()), 111)

    def test_create_wallet_for_new_account_and_delete_account_wallets(self):
        account = Account.Account(TEST_EMAIL3)
        self.assertTrue(Account.known_email(TEST_EMAIL3))
        account.delete_account()
        self.assertFalse(Account.known_email(TEST_EMAIL3))

    def test_existing_account_contains_wallet(self):
        email = TEST_EMAIL1
        account = Account.Account(email)
        self.assertTrue(Account.known_email(email))
        wallet_key = TEST_WALLET_KEY1
        self.assertTrue(account.contains_wallet(wallet_key))
        new_key = Account.create_wallet_key()
        self.assertFalse(account.contains_wallet(new_key))
        
    def test_create_new_wallet_for_existing_account_and_delete_wallet(self):
        email = TEST_EMAIL1
        self.assertTrue(Account.known_email(email))
        account = Account.Account(email)
        new_wallet = account.new_wallet_key()
        self.assertTrue(account.contains_wallet(new_wallet))
        account.remove_wallet(new_wallet)
        self.assertFalse(account.contains_wallet(new_wallet))

    def test_import_wallet_for_new_account(self):
        import_key_ = Account.create_wallet_key()
        account = Account.Account(TEST_EMAIL3, import_key = import_key_)
        self.assertTrue(account.contains_wallet(import_key_))

    def test_derive_child_from_wallet_key(self):
        account = Account.Account(TEST_EMAIL1)
        wallet = Wallet.Wallet.from_wallet_key(account.get_wallet_keys()[0])
        subkey = wallet.subkey().hwif()
        self.assertEqual('xpub68JyWgiDsfyPDroyVmeYKkTp2CDL5QQ4sfYbLxqZEGs7eQVQAWJHzumB4EL8oEzaqNFSYba2MS21Zo3DA8pU2iCp93EtHR1bZW8N7evXbs5', subkey)

    def test_derive_address_and_private_key_from_wallet_key(self):
        account = Account.Account(TEST_EMAIL1)
        wallet = Wallet.Wallet.from_wallet_key(account.get_wallet_keys()[0])
        self.assertEqual(48127745670158140224676891053325956567208697269841885640624450352410061813546, wallet.secret_exponent())
        self.assertEqual('16EbFsiGJzP6nJA3tFT9umsBrp4Asgt4XH', wallet.address())
        #secret_exponent = 48127745670158140224676891053325956567208697269841885640624450352410061813546
        #address = 16EbFsiGJzP6nJA3tFT9umsBrp4Asgt4XH


        
        
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

#returns the coinbase tx as hex. Used as an UTXO to test Txs
def coinbase():
    account = Account.Account(TEST_EMAIL1)
    wallet = Wallet.Wallet.from_wallet_key(account.get_wallet_keys()[0])
    address = wallet.address()
    assert is_address_valid(address)
    tx_in = TxIn.coinbase_tx_in(script=b'')
    tx_out = TxOut(50*1e8, standard_tx_out_script(address))
    tx = Tx(1, [tx_in], [tx_out])
    return tx.as_hex()

        
if __name__ == '__main__':
    unittest.main()

    
