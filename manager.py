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
        Create a new Account object with unique mpid
        """
        mpid = "mpid_0" #starting mpid
        if len(self._mpids) > 0:
            last_num = int(self._mpids[-1].split("_")[-1])
            mpid = f"mpid_{last_num + 1}"

        self._mpids.append(mpid)
        self._accounts.append(Account(mpid))

    def save_accounts(self):
        """
        Write account info to file at the end of a session.
        Assumes self.accounts is a list of Account objects and self.mp_ids is a list of corresponding MPID strings.
        """
        with open(self._filepath, 'w', encoding='utf-8') as file:
            data = {self._mpids[i]: self._accounts[i].__dict__ for i in range(len(self._mpids))}
            json.dump(data, file, indent=4)

    def get_trader(self, mpid):
        """Retrieve a trader by their mpid."""
        idx = int(mpid.split("_")[-1])
        return self._accounts[idx]

#manual testing
if __name__ == "__main__":
    manager = Manager("accounts.json")
    print(manager.get_mpids())
    print(manager.get_accounts())
    
    manager.create_account()
    print(manager.get_mpids())
    print(manager.get_accounts())
    manager.create_account()
    print(manager.get_mpids())
    print(manager.get_accounts())
    print(manager.get_accounts()[0].get_balance())
    manager.save_accounts()