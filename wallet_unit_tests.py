import unittest
import wallet

class WalletTests(unittest.TestCase):
    def test_get_test_wallet_key_by_email(self):
        test_email = 'jmdelaney8@gmail.com'
        test_wallet_key = 'xpub661MyMwAqRbcFCfnPWXdSgCTfhXqvkzBRU5wfths7Fnm45ypp2KBFB6UwVdyy4d1rMTuxNRAhaYRRU6oEkzDfujTELLa9MEFyYjXrtuyLRc'
        return self.assertEqual(test_wallet_key, wallet.get_wallet_key_by_email(test_email))


if __name__ == '__main__':
    unittest.main()
