from typing import Tuple, List, Dict
import os
import json
from account import Account

ADMIN_KEY = "ADMIN"

class Manager:
    """
    Account manager classes generated for each session. Loads prexisting accounts from file 
    and handles account creation and account saving to file.
    """
    
    def __init__(self, filepath: str):
        """
        Constructor for Manager class that loads preexisting account data
        Args:
            filepath (str): local filepath to preexisting account data
        """
        self.__filepath = filepath
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
            old_bal = self.__accounts_dict[mpid].get_balance(ADMIN_KEY)
            self.__accounts_dict[mpid].set_balance(ADMIN_KEY, old_bal + amount)
            return self.__accounts_dict[mpid].get_balance(ADMIN_KEY)
        else:
            raise ValueError("MPID does not exist")
    
    # def trade_position(self, mpid_b, mpid_s, trade):
    #     """
    #     Clearing house handles trades and can add positions to Accounts
    #     Args:
    #         mpid_b: mpid of buyer account to add position
    #         mpid_s: mpid of sell account to sell position
    #         trade: underlying position to trade
    #     """
    #     if mpid_b in self._accounts_dict and mpid_s in self._accounts_dict:
    #         seller = self._accounts_dict[mpid_s]
    #         buyer = self._accounts_dict[mpid_b]

    #         if trade in seller._open_positions:
    #             seller._open_positions.remove(trade)
    #             buyer._open_positions.append(trade)
    #         else:
    #             raise ValueError("Seller does not have position to sell") 
    #     else:
    #         raise ValueError("Buyer or Seller MPID does not exist")
    
    def add_position(self, mpid: str, trade, long: bool):
        """
        Add trade position either long or short to mpid's account
        Args:
            mpid: MPID of user to add trade to
            trade: underlying trade to add
            long: TRUE if long position FALSE if short position
        """
        if mpid in self.__accounts_dict:
            self.__accounts_dict[mpid].add_position(ADMIN_KEY, trade, long)
        else:
            raise ValueError("MPID does not exist")
    

    def load_accounts(self) -> Tuple[List[Account], List[str]]:
        """
        Loads accounts from preexisting account data from self.filepath
        """
        if not os.path.exists(self.__filepath):
            return {}
        
        try:
            with open(self.__filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            return {}
        
        accounts_dict = {mpid: Account(**details) for mpid, details in data.items()}
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

        new_acc = Account(mpid)
        self.__accounts_dict[mpid] = new_acc
        return new_acc.get_password(ADMIN_KEY)

    def save_accounts(self):
        """
        Save account info to file
        """
        with open(self.__filepath, 'w', encoding='utf-8') as file:
            data = {mpid: {
                    "mpid": acc.get_mpid(ADMIN_KEY),
                    "balance": acc.get_balance(ADMIN_KEY),
                    "past_trades": acc.get_past_trades(ADMIN_KEY),
                    "long_positions": acc.get_long_positions(ADMIN_KEY),
                    "short_positions": acc.get_short_positions(ADMIN_KEY),
                    "password": acc.get_password(ADMIN_KEY)
                } for mpid, acc in self.__accounts_dict.items()}
            
            json.dump(data, file, indent=4)

# manual testing
if __name__ == "__main__":
    manager = Manager("accounts.json")
    manager.create_account()
    manager.create_account()
    # acc0 = manager.get_accounts()[0]
    # acc1 = manager.get_accounts()[1]
    # acc0.add_position("TPC0")
    # manager.trade_position("MPID0", "MPID1", "TPC0")
    # print(manager.get_accounts()[0].get_positions("+>UQmAOP%M:OF:JK"))
    # print(manager.get_accounts()[1].get_positions("X~dd(usk8J%$L&pv"))
    manager.save_accounts()