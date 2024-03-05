from trademessage import *
from manager import Manager
import toml

class ClearingHouse:

    def __init__(self, trade_filepath: str, acc_filepath: str):
        self._trade_filepath = trade_filepath
        self._acc_filepath = acc_filepath
        self._trade_processor = TradeProcessing()
        self._trade_processor.read_previous_trades_txt(self._trade_filepath)
        self._acc_manager = Manager(self._acc_filepath)
        self._securities = toml.load("securities.toml")['securities']

    def receive_new_contract(self, trade_message: TradeMessage):
        self._trade_processor.read_new_trade(trade_message)
        buyer_mpid = trade_message.buyer_mpid
        seller_mpid = trade_message.seller_mpid
        price = trade_message.price
        ticker = trade_message.ticker[:4]
        decimals = self._securities[ticker]['decimals']
        lot = self._securities[ticker]['lot']
        self.execute_cash_trade(buyer_mpid, seller_mpid, (-1.0 * price) / pow(10, decimals))
        self.execute_security_trade(buyer_mpid, seller_mpid, ticker, trade_message.volume * lot)

    def on_turn(self, turn_num: int, price: int):
        trade_data = self._trade_processor.get_trades()
        for trade_info in trade_data:
            if (trade_info == None or trade_info.isSettled()): # settled
                continue

            buy_turn = trade_info.getBuyTurn()
            sell_turn = trade_info.getSellTurn()
            trade_message = trade_info.getTradeMessage()
            buyer_mpid = trade_message.get_buyer_mpid()
            seller_mpid = trade_message.get_seller_mpid()
            volume = trade_message.get_volume()
            ticker = trade_message.get_ticker()[:4]
            decimals = self._securities[ticker]['decimals']
            lot = self._securities[ticker]['lot']

            if (buy_turn == turn_num and buy_turn == sell_turn): # not a spread
                price_change = ((price * lot) - (trade_message.get_price() * (lot - 1))) * volume / pow(10, decimals)
                self.execute_cash_trade(buyer_mpid, seller_mpid, price_change)
                self.execute_security_trade(buyer_mpid, seller_mpid, ticker, -1 * volume * lot)
                self._trade_processor.set_to_settled(trade_message.get_trade_id())

            else: # spread
                if (buy_turn == turn_num):
                    if (buy_turn > sell_turn): # short sell, settling
                        price_change = volume * price * lot / pow(10, decimals)
                        self.execute_cash_trade(buyer_mpid, seller_mpid, -1 * price_change)
                        self.execute_security_trade(buyer_mpid, seller_mpid, ticker, volume * lot)
                        self._trade_processor.set_to_settled(trade_message.get_trade_id())
                        
                    else: # regular, not settling
                        price_change = volume * trade_message.get_price() * (lot - 1) / pow(10, decimals)
                        self.execute_cash_trade(buyer_mpid, seller_mpid, -1 * price_change)
                        self.execute_security_trade(buyer_mpid, seller_mpid, ticker, volume * lot)

                if (sell_turn == turn_num):
                    if (buy_turn > sell_turn): # sell short, not settling
                        price_change = volume * trade_message.get_price() * (lot - 1) / pow(10, decimals)
                        self.execute_cash_trade(buyer_mpid, seller_mpid, price_change)
                        self.execute_security_trade(buyer_mpid, seller_mpid, ticker, -1 * volume * lot)

                    else: # regular, settling
                        price_change = volume * price * lot / pow(10, decimals)
                        self.execute_cash_trade(buyer_mpid, seller_mpid, price_change)
                        self.execute_security_trade(buyer_mpid, seller_mpid, ticker, -1 * volume * lot)
                        self._trade_processor.set_to_settled(trade_message.get_trade_id())

    def execute_cash_trade(self, buyer_mpid, seller_mpid, buyer_price_change):
        buyer_balance = self._acc_manager.modify_balance(buyer_mpid, buyer_price_change)
        seller_balance = self._acc_manager.modify_balance(seller_mpid, -1 * buyer_price_change)
        print("Account", buyer_mpid, "balance is now", buyer_balance)
        print("Account", seller_mpid, "balance is now", seller_balance)

    def execute_security_trade(self, buyer_mpid, seller_mpid, security, buyer_volume_change):
        buyer_holding = self._acc_manager.update_account_security_volume(buyer_mpid, security, buyer_volume_change)
        seller_holding = self._acc_manager.update_account_security_volume(seller_mpid, security, -1 * buyer_volume_change)
        print("Account", buyer_mpid, "holding of", security, "is now", buyer_holding)
        print("Account", seller_mpid, "holding of", security, "is now", seller_holding)

    def end_session(self):
        self._acc_manager.save_accounts()


if __name__ == "__main__":
    clearinghouse = ClearingHouse("testin.txt", "accounts.json")
    clearinghouse.on_turn(6, 200)
    clearinghouse.on_turn(2, 160)
    clearinghouse.end_session()