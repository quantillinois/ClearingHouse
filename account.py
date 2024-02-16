import random
import string
from typing import List

PASSWORD_LENGTH = 16
ADMIN_KEY = "ADMIN"

class Account:
    """
    Account class is for each trader, storing their mpid, balance, past_trades, long_positions, and password
    """
    
    def __init__(self, mpid: str, balance: int = 1000000, past_trades: List = None, long_positions: List = None, short_positions: List = None, password: str = None):
        self.__mpid = mpid
        self.__balance = balance
        self.__past_trades = past_trades if past_trades is not None else []
        self.__long_positions = long_positions if long_positions is not None else []
        self.__short_positions = short_positions if short_positions is not None else []
        self.__password = password if password is not None else generate_password()
    
    def get_mpid(self, password: str) -> str:
        """
        Gets mpid if user password or admin key is provided
        """
        if self.__password == password or password == ADMIN_KEY:
            return self.__mpid
        else:
            raise ValueError("Incorrect password")
        
    def get_balance(self, password: str) -> int:
        """
        Gets the balance if user password or admin key is provided
        """
        if self.__password == password or password == ADMIN_KEY:
            return self.__balance
        else:
            raise ValueError("Incorrect password")
    def set_balance(self, admin_key: str, new_bal: int):
        """
        Sets the balance only if admin key is provided
        """
        if admin_key == ADMIN_KEY:
            self.__balance = new_bal
        else:
            raise ValueError("Incorrect password")
        
    def add_position(self, admin_key: str, trade, long: bool):
        """
        Adds position only if admin password is provided
        Args:
            admin_key(str): admin password for access
            trade: underlying trade to add
            long(bool): TRUE if long position FALSE if short position
        """
        if admin_key == ADMIN_KEY:
            if long:
                self.__long_positions.append(trade)
            else:
                self.__short_positions.append(trade)
        else:
            raise ValueError("Incorrect password")
            
    def get_long_positions(self, password: str) -> List:
        """
        Returns long positions given user password or admin password
        """
        if self.__password == password or password == ADMIN_KEY:
            return self.__long_positions
        else:
            raise ValueError("Incorrect password")
    
    def get_short_positions(self, password: str) -> List:
        """
        Returns short positions given user password or admin password
        """
        if self.__password == password or password == ADMIN_KEY:
            return self.__short_positions
        else:
            raise ValueError("Incorrect password")

    def get_past_trades(self, password: str):
        """
        Returns pass trades given user password or admin password
        """
        if self.__password == password or password == ADMIN_KEY:
            return self.__past_trades
        else:
            raise ValueError("Incorrect password")
    
    def get_password(self, admin_key: str):
        """
        Returns user password
        """
        if admin_key == ADMIN_KEY:
            return self.__password
        else:
            raise ValueError("Incorrect password")
    
def generate_password():
    """
    Generates random 16 byte password for account
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(PASSWORD_LENGTH))
    return password