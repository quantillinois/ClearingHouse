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

class TradeInfo:
    def __init__(self, trade: TradeMessage, buy_turn: int, sell_turn: int, settled: bool):
        self.trade = trade
        self.buy_turn = buy_turn
        self.sell_turn = sell_turn
        self.settled = settled

class TradeProcessing:
    def __init__(self):
        self.trade_data = []
        self.trade_id_count = 0 

    #private helper function to read from a txt file
    def __read_trades_txt(self, file):
        with open(file, 'r') as file:
            for line in file:
                trade_data_str = line.strip().replace("TradeMessage(", "").replace(")", "")
                # Enclose attribute names in quotes to make it a valid dictionary string
                trade_data_str = trade_data_str.replace('ticker=', '"ticker":').replace('timestamp=', '"timestamp":').replace('price=', '"price":').replace('volume=', '"volume":').replace('buyer_mpid=', '"buyer_mpid":').replace('buyer_order_id=', '"buyer_order_id":').replace('seller_mpid=', '"seller_mpid":').replace('seller_order_id=', '"seller_order_id":').replace('trade_id=', '"trade_id":').replace('buy_turn=', '"buy_turn":').replace('sell_turn=', '"sell_turn":').replace('settled=', '"settled":')
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
                buy_turn = int(trade_data.get('buy_turn'))
                sell_turn = int(trade_data.get('sell_turn'))
                if trade_data.get('settled') == "True":
                    settled = True
                else:
                    settled = False
                # Create TradeMessage object
                trade = TradeMessage(ticker, timestamp, price, volume, buyer_mpid, buyer_order_id, seller_mpid, seller_order_id, trade_id)
                self.trade_data.append(TradeInfo(trade,buy_turn,sell_turn,settled))
                self.trade_id_count+=1

    def read_previous_trades_txt(self, pasttradefile):
        self.__read_trades_txt(pasttradefile)
        return self.trade_data
    
    def read_new_trades(self, newtrade):
        buy_turn = int(newtrade.ticker[4:6])
        sell_turn = int(newtrade.ticker[-2:])
        settled = self.is_settled(newtrade.trade_id)
        self.trade_data.append(TradeInfo(newtrade,buy_turn,sell_turn,settled))
        self.trade_id_count+=1

    def is_settled(self, trade_id):
        return True  # Placeholder for actual implementation

    def write_trades_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for trade_info in self.trade_data:
                writetrade = trade_info.trade
                ticker = writetrade.ticker
                timestamp = writetrade.timestamp
                price = writetrade.price
                volume = writetrade.volume
                buyer_mpid = writetrade.buyer_mpid
                buyer_order_id = writetrade.buyer_order_id
                seller_mpid = writetrade.seller_mpid
                seller_order_id = writetrade.seller_order_id
                trade_id = writetrade.trade_id 

                buy_turn = trade_info.buy_turn
                sell_turn = trade_info.sell_turn
                settled = trade_info.settled

                # Create the TradeMessage string
                trade_message_str = f"TradeMessage(ticker='{ticker}', timestamp={timestamp}, price={price}, volume={volume}, buyer_mpid='{buyer_mpid}', buyer_order_id='{buyer_order_id}', seller_mpid='{seller_mpid}', seller_order_id='{seller_order_id}', trade_id='{trade_id}')"

                # Create the additional attributes string
                additional_attributes_str = f", buy_turn='{buy_turn}', sell_turn='{sell_turn}', settled='{settled}'"
                # Combine both strings
                trade_str = trade_message_str + additional_attributes_str + "\n"
                file.write(trade_str)
            self.trade_data.clear()
            self.trade_id_count = 0

        def get_ticker(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.ticker
            else:
                return None

        def get_timestamp(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.timestamp
            else:
                return None

        def get_price(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.price
            else:
                return None

        def get_volume(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.volume
            else:
                return None

        def get_buyer_mpid(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.buyer_mpid
            else:
                return None

        def get_buyer_order_id(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.buyer_order_id
            else:
                return None

        def get_seller_mpid(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.seller_mpid
            else:
                return None

        def get_seller_order_id(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.seller_order_id
            else:
                return None

        def get_trade_id(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].trade.trade_id
            else:
                return None
        
        def get_buy_turn(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].buy_turn
            else:
                return None
            
        def get_sell_turn(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].sell_turn
            else:
                return None
            
        def get_settled(self, index):
            if 0 <= index <= self.trade_id_count:
                return self.trade_data[index].settled
            else:
                return None

#testing
if __name__ == "__main__":
    trade_processor = TradeProcessing()
    trade_processor.read_previous_trades_txt("testin.txt")
    trade_processor.read_new_trades(TradeMessage(ticker='TPCF0817', timestamp=8, price=100, volume=90, buyer_mpid='MPID1', buyer_order_id='None', seller_mpid='None', seller_order_id='0000000003', trade_id='18'))
    trade_processor.read_new_trades(TradeMessage(ticker='TPCF0521', timestamp=5, price=95, volume=100, buyer_mpid='MPID1', buyer_order_id='None', seller_mpid='None', seller_order_id='0000000003', trade_id='14'))
    trade_processor.read_new_trades(TradeMessage(ticker='TPCF1028', timestamp=10, price=105, volume=110, buyer_mpid='MPID1', buyer_order_id='None', seller_mpid='None', seller_order_id='0000000003', trade_id='23'))
    trade_processor.write_trades_to_file("testout.txt")


