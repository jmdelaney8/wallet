from pycoin.key.BIP32Node import BIP32Node
from pycoin.cmds import ku

from smtplib import SMTP_SSL
import sqlite3

class Wallet(BIP32Node):
    def donothing(self):
        return
