import ast 

class TradeMessage:
    def __init__(self, ticker, timestamp, price, volume, buyer_mpid, buyer_order_id, seller_mpid, seller_order_id, trade_id):
        self.ticker = ticker
        self.timestamp = timestamp
        self.price = price
        self.volume = volume
        self.buyer_mpid = buyer_mpid
        self.buyer_order_id = buyer_order_id
        self.seller_mpid = seller_mpid
        self.seller_order_id = seller_order_id
        self.trade_id = trade_id


class TradeProcessing:
    def __init__(self):
        self.trade_data = []
    def __read_trades_txt(self, file):
        with open(file, 'r') as file:
            for line in file:
                trade_data_str = line.strip().replace("TradeMessage(", "").replace(")", "")
                # Enclose attribute names in quotes to make it a valid dictionary string
                trade_data_str = trade_data_str.replace('ticker=', '"ticker":').replace('timestamp=', '"timestamp":').replace('price=', '"price":').replace('volume=', '"volume":').replace('buyer_mpid=', '"buyer_mpid":').replace('buyer_order_id=', '"buyer_order_id":').replace('seller_mpid=', '"seller_mpid":').replace('seller_order_id=', '"seller_order_id":').replace('trade_id=', '"trade_id":')
                trade_data = ast.literal_eval("{" + trade_data_str + "}")

                ticker = trade_data.get('ticker')
                timestamp = int(trade_data.get('timestamp'))
                price = int(trade_data.get('price'))
                volume = int(trade_data.get('volume'))
                buyer_mpid = trade_data.get('buyer_mpid')
                buyer_order_id = trade_data.get('buyer_order_id')
                seller_mpid = trade_data.get('seller_mpid')
                seller_order_id = trade_data.get('seller_order_id')
                trade_id = trade_data.get('trade_id')

                # Create TradeMessage object
                trade = TradeMessage(ticker, timestamp, price, volume, buyer_mpid, buyer_order_id, seller_mpid, seller_order_id, trade_id)
                buy_turn = int(ticker[4:6])
                sell_turn = int(ticker[-2:])
                settled = self.is_settled(trade_id)
                self.trade_data.append([trade, buy_turn, sell_turn, settled])

    def read_trades_txt(self, infile, pasttradefile):
        self.__read_trades_txt(pasttradefile)
        self.__read_trades_txt(infile)
        return self.trade_data


    def is_settled(self, trade_id):
        return True  # Placeholder for actual implementation

    def write_trades_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for trade_info in self.trade_data:
                trade = trade_info[0]
                ticker = trade.ticker
                timestamp = trade.timestamp
                price = trade.price
                volume = trade.volume
                buyer_mpid = trade.buyer_mpid
                buyer_order_id = trade.buyer_order_id
                seller_mpid = trade.seller_mpid
                seller_order_id = trade.seller_order_id
                trade_id = trade.trade_id
        
                trade_str = f"TradeMessage(ticker='{ticker}', timestamp={timestamp}, price={price}, volume={volume}, buyer_mpid='{buyer_mpid}', buyer_order_id='{buyer_order_id}', seller_mpid='{seller_mpid}', seller_order_id='{seller_order_id}', trade_id='{trade_id}')\n"
                file.write(trade_str)
            self.trade_data.clear()


#testing
if __name__ == "__main__":
    trade_processor = TradeProcessing()
    trade_processor.read_trades_txt("testin.txt","testout.txt")
    trade_processor.write_trades_to_file("testout.txt")
    trade_processor.read_trades_txt("testin2.txt","testout.txt")
    trade_processor.write_trades_to_file("testout.txt")