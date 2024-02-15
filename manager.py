from typing import Tuple, List
import os
import json
from account import Account

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
        self._accounts, self._mpids = self.load_accounts()

    def get_mpids(self) -> List[str]:
        """
        Getter for _mpid attribute
        """
        return self._mpids
    
    def get_accounts(self) -> List[Account]:
        """
        Getter for _accounts attribute
        """
        return self._accounts
    
    def modify_balance(self, mpid, amount):
        """
        Clearing house has access to modify balance of accounts.
        Args:
            mpid: mpid of account to modify balance
            amount: net change of amount to reflect to account
        """
        if mpid in self._mpids:
            idx = self._mpids.index(mpid)
            self._accounts[idx]._balance += amount
            return self._accounts[idx]._balance
        else:
            raise ValueError("MPID does not exist")
    def trade_position(self, mpid_b, mpid_s, trade):
        """
        Clearing house handles trades and can add positions to Accounts
        Args:
            mpid_b: mpid of buyer account to add position
            mpid_s: mpid of sell account to sell position
            trade: underlying position to trade
        """
        if mpid_b in self._mpids and mpid_s in self._mpids:
            seller_idx = self._mpids.index(mpid_s)
            buyer_idx = self._mpids.index(mpid_b)

            if trade in self._accounts[seller_idx]._open_positions:
                trade_idx = self._accounts[seller_idx]._open_positions.index(trade)
                del self._accounts[seller_idx]._open_positions[trade_idx]
                self._accounts[buyer_idx]._open_positions.append(trade)
            else:
                raise ValueError("MPID_s does not have position to sell") 
        else:
            raise ValueError("MPID_b or MPID_s does not exist")
    
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
            return [], []
        
        try:
            with open(self._filepath, 'r', encoding='utf-8') as file:
                # Attempt to load the file
                data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {}
        #print(data)
        accounts = []
        mpids = []
        for mpid, details in data.items():
            accounts.append(Account(**details))
            mpids.append(mpid)
            
        return accounts, mpids

    def create_account(self):
        """
        Create a new Account object with unique mpid in the format "MPID1"
        """
        mpid = "MPID0"  # Starting mpid
        if len(self._mpids) > 0:
            last_num = int(self._mpids[-1][4:]) 
            mpid = f"MPID{last_num + 1}"

        self._mpids.append(mpid)
        new_acc = Account(mpid)
        self._accounts.append(new_acc)
        return new_acc._password

    def save_accounts(self):
        """
        Write account info to file at the end of a session.
        Converts account object attributes to a dictionary without leading underscores in keys.
        """
        with open(self._filepath, 'w', encoding='utf-8') as file:
            data = {}
            for i in range(len(self._mpids)):
                account = self._accounts[i]
                account_data = {
                    "mpid": account._mpid,
                    "balance": account._balance,
                    "past_trades": account._past_trades,
                    "open_positions": account._open_positions,
                    "password": account._password
                }
                data[self._mpids[i]] = account_data
            
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
    # manager.create_account()
    # manager.create_account()
    acc0 = manager.get_accounts()[0]
    acc1 = manager.get_accounts()[1]
    manager.create_account()
    # acc0.add_position("TPC0")
    # manager.trade_position("MPID0", "MPID1", "TPC0")
    # print(manager.get_accounts()[0].get_positions("+>UQmAOP%M:OF:JK"))
    # print(manager.get_accounts()[1].get_positions("X~dd(usk8J%$L&pv"))
    manager.save_accounts()