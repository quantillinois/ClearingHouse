import random
import string

PASSWORD_LENGTH = 16

class Account:
    """
    Account class is for each trader, storing their mpid, balance, past_trades, open_positions, and password
    """
    
    def __init__(self, mpid, balance=1000000, past_trades=None, open_positions=None, password=None):
        self.mpid = mpid
        self.balance = balance
        self.past_trades = past_trades if past_trades is not None else []
        self.open_positions = open_positions if open_positions is not None else []
        self.password = password if password is not None else self.generate_password()
    
    def get_balance(self):
        return self.balance
    
    def set_balance(self, new_bal):
        self.balance = new_bal
        
    def get_positions(self):
        return self.open_positions

    def get_past_transactions(self):
        return self.past_trades
    
    def generate_password(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(chars) for i in range(PASSWORD_LENGTH))
        print(password)
        return password
    