from pycoin.key.BIP32Node import BIP32Node as node

password1 = "password"
password1_enc = password1.encode('utf-8')

wallet1 = node.from_master_secret(password1_enc)

print( wallet1)

password2 = "password"
password2_enc = password2.encode('utf-8')

wallet2 = node.from_master_secret(password2_enc)
print(wallet2.wallet_key())

print(wallet1.wallet_key() == wallet2.wallet_key())


print(wallet1.fingerprint() == node.from_wallet_key(wallet2.wallet_key()).fingerprint())
