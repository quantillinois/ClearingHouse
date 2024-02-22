from typing import List, Dict, Tuple

class Account:
    """
    Account class is for each trader, storing their mpid, balance, past_trades, long_positions, and password
    """
    
    def __init__(self, mpid: str, password: str, balance: int, past_trades: List, positions: Dict[str, int]):
        self.__mpid = mpid
        self.__password = password
        self.__balance = balance
        self.__past_trades = past_trades
        self.__positions = positions
        
    
    def get_mpid(self) -> str:
        """
        Getter for mpid
        """
        return self.__mpid

        
    def get_balance(self) -> int:
        """
        Getter for balance
        """
        return self.__balance

        
    def set_balance(self, new_bal: int):
        """
        Sets the balance to new value
        """
        self.__balance = new_bal

    

    def add_position(self, ticker: str, volume: int):
        """
        Adds position to account
        Args:
            trade(str): underlying trade to add
            volume(int): positive volume for long, negative volume for short positions
        """

        self.__positions[ticker] += volume
    
    def add_past_trade(self, trade):
        """
        Appends past trade to list of past trades
        """
        self.__past_trades.append(trade)

    def get_positions(self) -> Dict[str, int]:
        """
        Getter for all positions
        """
        return self.__positions
            
    def get_long_positions(self) -> List[Tuple[str, int]]:
        """
        Returns long positions
        """
        long = []
        for ticker, volume in self.__positions.items():
            if volume > 0:
                long.append((ticker, volume))
        
        return long

    
    def get_short_positions(self) -> List[Tuple[str, int]]:
        """
        Returns short positions
        """
        short = []
        for ticker, volume in self.__positions.items():
            if volume < 0:
                short.append((ticker, volume))
        
        return short

    def get_past_trades(self):
        """
        Returns past trades
        """
        return self.__past_trades
    
    def get_password(self):
        """
        Returns user password
        """
        return self.__password
    
