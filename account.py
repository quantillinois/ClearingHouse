import random
import string
import typing

PASSWORD_LENGTH = 16

class Account:
    """
    Account class is for each trader, storing their mpid, balance, past_trades, open_positions, and password
    """
    
    def __init__(self, mpid, balance=1000000, past_trades=None, open_positions=None, password=None):
        self._mpid = mpid
        self._balance = balance
        self._past_trades = past_trades if past_trades is not None else []
        self._open_positions = open_positions if open_positions is not None else []
        self._password = password if password is not None else self._generate_password()
    
    def get_balance(self, password):
        if self._password == password:
            return self._balance
        else:
            raise ValueError("Incorrect password")

    def get_positions(self, password):
        if self._password == password:
            return self._open_positions

    def get_past_transactions(self, password):
        if self._password == password:
            return self._past_trades
    
    def _generate_password(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for _ in range(PASSWORD_LENGTH))
        return password