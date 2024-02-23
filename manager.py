from typing import Tuple, List, Dict
import os
import random
import string
import json
import sqlite3
import hashlib
from collections import defaultdict
from account import Account

PASSWORD_LENGTH = 16
STARTING_BALANCE = 1000000

def generate_password():
    """
    Generates random 16 byte password for account
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(PASSWORD_LENGTH))
    return password

def hash_password(password: str) -> str:
    """
    Hashes a password using SHA-256 and returns the hexadecimal representation.
    """
    return hashlib.sha256(password.encode()).hexdigest()

class Manager:
    """
    Account manager classes generated for each session. Loads prexisting accounts from file 
    and handles account creation and account saving to file.
    """
    
    def __init__(self, db_path: str):
        """
        Constructor for Manager class that loads preexisting account data
        """
        self.__db_path = db_path
        self.conn = sqlite3.connect(self.__db_path)
        self.cursor = self.conn.cursor()

        self.__accounts_dict = self.load_accounts()

    def get_mpids(self) -> List[str]:
        """
        Getter for MPIDs
        """
        return list(self.__accounts_dict.keys())
    
    def get_accounts(self) -> List[Account]:
        """
        Getter for Account objects
        """
        return list(self.__accounts_dict.values())
    
    def get_account_dict(self) -> Dict[str, Account]:
        """
        Getter for Account dict
        """
        return self.__accounts_dict
    
    def modify_balance(self, mpid: str, amount: int) -> int:
        """
        Clearing house has access to modify balance of accounts.
        Args:
            mpid: mpid of account to modify balance
            amount: net change of amount to reflect to account
        """
        if mpid in self.__accounts_dict:
            old_bal = self.__accounts_dict[mpid].get_balance()
            self.__accounts_dict[mpid].set_balance(old_bal + amount)
            self.cursor.execute(("UPDATE accounts SET balance = ? WHERE mpid = ?"), (old_bal + amount, mpid))
            return self.__accounts_dict[mpid].get_balance()
        else:
            raise ValueError("MPID does not exist")
    
    def add_position(self, mpid: str, ticker: str, volume: int):
        """
        Add trade position either long or short to mpid's account
        Args:
            mpid: MPID of user to add trade to
            trade: underlying trade ticker to add
            volume: volume of trade
        """
        if mpid in self.__accounts_dict:
            self.__accounts_dict[mpid].add_position(ticker, volume)
            self.cursor.execute("INSERT INTO positions (mpid, ticker, volume) VALUES (?, ?, ?)",
                            (mpid, ticker, volume))
        else:
            raise ValueError("MPID does not exist")
    
    
    def load_accounts(self) -> Dict[str, Account]:
        """
        Load accounts from the SQLite database and instantiate Account objects for each.
        
        Returns:
            A dictionary mapping MPIDs to Account objects.
        """
        self.cursor.execute('''
                            SELECT a.mpid, a.password, a.balance, t.trade_details, p.ticker, p.volume
                            FROM accounts a
                            LEFT JOIN past_trades t ON a.mpid = t.mpid
                            LEFT JOIN positions p ON a.mpid = p.mpid
                            ''')
        rows = self.cursor.fetchall()
        accounts_dict = {}
        for row in rows:
            mpid, password, balance, trade_details, ticker, volume = row
            if mpid in accounts_dict:
                if ticker is not None and volume is not None:
                    accounts_dict[mpid].add_position(ticker, volume)
                if trade_details is not None:
                    accounts_dict[mpid].add_past_trade(trade_details)
            else:
                accounts_dict[mpid] = Account(mpid, password, balance, [], defaultdict(int))
        
        return accounts_dict

    def create_account(self) -> str:
        """
        Create a new Account object with unique mpid in the format "MPID0"

        Returns:
            password associated with created account
        """
        mpid = "MPID0"  # Starting mpid
        if self.__accounts_dict:
            last_num = max(int(mpid[4:]) for mpid in self.__accounts_dict.keys())
            mpid = f"MPID{last_num + 1}"
        password = generate_password()
        hashed_password = hash_password(password)
        new_acc = Account(mpid, password, STARTING_BALANCE, [], defaultdict(int))
        self.__accounts_dict[mpid] = new_acc
        self.cursor.execute("INSERT INTO accounts (mpid, password, balance) VALUES (?, ?, ?)",
                            (mpid, hashed_password, STARTING_BALANCE))
        return password

    def close(self):
        """
        Close the database connection.
        """
        self.conn.commit()
        self.conn.close()

# manual testing
if __name__ == "__main__":
    manager = Manager("accounts.db")
    # manager.create_account()
    # manager.create_account()
    print(manager.get_account_dict()['MPID0'].get_password())
    # manager.add_position("MPID0", "TPC1010", 5)

    manager.close()