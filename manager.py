from typing import Tuple, List
import os
import json
from account import Account
# from account import Position

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
        self._filepath = filepath
        self._accounts_dict = self.load_accounts()

    def get_mpids(self) -> List[str]:
        """
        Getter for MPIDs
        """
        return list(self._accounts_dict.keys())
    
    def get_accounts(self) -> List[Account]:
        """
        Getter for Account objects
        """
        return list(self._accounts_dict.values())
    
    def modify_balance(self, mpid, amount):
        """
        Clearing house has access to modify balance of accounts.
        Args:
            mpid: mpid of account to modify balance
            amount: net change of amount to reflect to account
        """
        if mpid in self._accounts_dict:
            self._accounts_dict[mpid]._balance += amount
            return self._accounts_dict[mpid]._balance
        else:
            raise ValueError("MPID does not exist")
    
    def update_account_security_volume(self, mpid, security, amount):
        positions = self._accounts_dict[mpid]._open_positions

        if (security in positions.keys()):
            positions[security] += amount
        else:
            positions[security] = amount

        return positions[security]

    def add_trade_to_accounts(self, mpid_b, mpid_s, trade_id):
        """
        Clearing house handles trades and can add trades to Accounts
        Args:
            mpid_b: mpid of buyer account
            mpid_s: mpid of sell account
            trade_id: TradeMessage
        """
        if mpid_b in self._accounts_dict and mpid_s in self._accounts_dict:
            seller = self._accounts_dict[mpid_s]
            buyer = self._accounts_dict[mpid_b]

            buyer._past_trades.append(trade_id)
            if (buyer != seller):
                seller._past_trades.append(trade_id)

        else:
            raise ValueError("Buyer or Seller MPID does not exist")
    
    #TODO
    def settle_positions(self, turn):
        """
        Clearing house must settle all positions after each turn and update balances, past_trades, and open_positions accordingly
        """
        pass

    def load_accounts(self) -> Tuple[List[Account], List[str]]:
        """
        Loads accounts from preexisting account data from self.filepath
        """
        if not os.path.exists(self._filepath):
            return {}
        
        try:
            with open(self._filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            return {}
        
        accounts_dict = {mpid: Account(**details) for mpid, details in data.items()}
        return accounts_dict

    def create_account(self):
        """
        Create a new Account object with unique mpid in the format "MPID0"
        """
        mpid = "MPID0"  # Starting mpid
        if self._accounts_dict:
            last_num = max(int(mpid[4:]) for mpid in self._accounts_dict.keys())
            mpid = f"MPID{last_num + 1}"

        new_acc = Account(mpid)
        self._accounts_dict[mpid] = new_acc
        return new_acc._password

    def save_accounts(self):
        """
        Save account info to file
        """
        with open(self._filepath, 'w', encoding='utf-8') as file:
            data = {mpid: {
                    "mpid": acc._mpid,
                    "balance": acc._balance,
                    "past_trades": acc._past_trades,
                    "open_positions": acc._open_positions,
                    "password": acc._password
                } for mpid, acc in self._accounts_dict.items()}
            
            json.dump(data, file, indent=4)

    def get_trader(self, mpid):
        """
        Retrieve a trader by their mpid
        """
        idx = int(mpid[4:])
        return self._accounts[idx]

# manual testing
if __name__ == "__main__":
    manager = Manager("accounts.json")
    manager.load_accounts()
    # manager.create_account()
    # manager.create_account()
    # manager.create_account()
    manager.update_account_security_volume("MPID1", "TPC", 100)
    # acc0 = manager.get_accounts()[0]
    # acc1 = manager.get_accounts()[1]
    # acc0.add_position("TPC0")
    # manager.trade_position("MPID0", "MPID1", "TPC0")
    # print(manager.get_accounts()[0].get_positions("+>UQmAOP%M:OF:JK"))
    # print(manager.get_accounts()[1].get_positions("X~dd(usk8J%$L&pv"))
    manager.save_accounts()


# from typing import Tuple, List
# import os
# import json
# from account import Account

# class Manager:
#     """
#     Account manager classes generated for each session. Loads prexisting accounts from file 
#     and handles account creation and account saving to file.
#     """
    
#     def __init__(self, filepath: str):
#         """
#         Constructor for Manager class that loads preexisting account data
#         Args:
#             filepath (str): local filepath to preexisting account data
#         """
#         self._filepath = filepath
#         self._accounts, self._mpids = self.load_accounts()

#     def get_mpids(self) -> List[str]:
#         """
#         Getter for _mpid attribute
#         """
#         return self._mpids
    
#     def get_accounts(self) -> List[Account]:
#         """
#         Getter for _accounts attribute
#         """
#         return self._accounts
    
#     def load_accounts(self) -> Tuple[List[Account], List[str]]:
#         """
#         Loads accounts from preexisting account data from self.filepath
#         """
#         if not os.path.exists(self._filepath):
#             return [], []
        
#         try:
#             with open(self._filepath, 'r', encoding='utf-8') as file:
#                 # Attempt to load the file
#                 data = json.load(file)
#         except json.decoder.JSONDecodeError:
#             data = {}
#         #print(data)
#         accounts = []
#         mpids = []
#         for mpid, details in data.items():
#             accounts.append(Account(**details))
#             mpids.append(mpid)
            
#         return accounts, mpids

#     def create_account(self):
#         """
#         Create a new Account object with unique mpid
#         """
#         mpid = "mpid_0" #starting mpid
#         if len(self._mpids) > 0:
#             last_num = int(self._mpids[-1].split("_")[-1])
#             mpid = f"mpid_{last_num + 1}"

#         self._mpids.append(mpid)
#         self._accounts.append(Account(mpid))

#     def save_accounts(self):
#         """
#         Write account info to file at the end of a session.
#         Assumes self.accounts is a list of Account objects and self.mp_ids is a list of corresponding MPID strings.
#         """
#         with open(self._filepath, 'w', encoding='utf-8') as file:
#             data = {self._mpids[i]: self._accounts[i].__dict__ for i in range(len(self._mpids))}
#             json.dump(data, file, indent=4)

#     def get_trader(self, mpid):
#         """Retrieve a trader by their mpid."""
#         idx = int(mpid.split("_")[-1])
#         return self._accounts[idx]

#     def update_account_balance(self, mpid, delta: int):
#         account = self.get_trader(mpid)
#         account.set_balance(account.get_balance() + delta)

#     def get_account_balance(self, mpid):
#         return self.get_trader(mpid).get_balance()

# #manual testing
# if __name__ == "__main__":
#     manager = Manager("accounts.json")
#     print(manager.get_mpids())
#     print(manager.get_accounts())
    
#     manager.create_account()
#     print(manager.get_mpids())
#     print(manager.get_accounts())
#     manager.create_account()
#     print(manager.get_mpids())
#     print(manager.get_accounts())
#     print(manager.get_accounts()[0].get_balance())
#     manager.save_accounts()