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

    def get_volume(self):
        return self.volume

    def get_price(self):
        return self.price

    def get_trade_id(self):
        return self.trade_id

    def get_buyer_mpid(self):
        return self.buyer_mpid

    def get_seller_mpid(self):
        return self.seller_mpid
    
    def get_ticker(self):
        return self.ticker

class TradeInfo:
    def __init__(self, trade: TradeMessage, buy_turn: int, sell_turn: int, settled: bool):
        self.trade = trade
        self.buy_turn = buy_turn
        self.sell_turn = sell_turn
        self.settled = settled

    def isSettled(self):
        return self.settled

    def getTradeMessage(self):
        return self.trade
    
    def getBuyTurn(self):
        return self.buy_turn
    
    def getSellTurn(self):
        return self.sell_turn

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
                trade_id = int(trade_data.get('trade_id'))
                buy_turn = int(trade_data.get('buy_turn'))
                sell_turn = int(trade_data.get('sell_turn'))
                if trade_data.get('settled') == "True":
                    settled = True
                else:
                    settled = False
                # Create TradeMessage object
                trade = TradeMessage(ticker, timestamp, price, volume, buyer_mpid, buyer_order_id, seller_mpid, seller_order_id, trade_id)
                if trade_id > self.trade_id_count:
                    for _ in range(trade_id - self.trade_id_count):
                        self.trade_data.append(None)
                    self.trade_id_count = trade_id
                self.trade_data.append(TradeInfo(trade,buy_turn,sell_turn,settled))
                self.trade_id_count=self.trade_id_count+1

    def read_previous_trades_txt(self, pasttradefile):
        self.__read_trades_txt(pasttradefile)
        return self.trade_data
    
    def read_new_trade(self, newtrade):
        buy_turn = int(newtrade.ticker[4:6])
        sell_turn = int(newtrade.ticker[-2:])
        settled = self.is_settled(newtrade.trade_id)
        if int(newtrade.trade_id) > self.trade_id_count:
            for _ in range(int(newtrade.trade_id) - self.trade_id_count):
                self.trade_data.append(None)
            self.trade_id_count = int(newtrade.trade_id)
        self.trade_data.append(TradeInfo(newtrade,buy_turn,sell_turn,settled))
        self.trade_id_count+=1

    def get_trades(self):
        return self.trade_data
    
    def set_to_settled(self, trade_id):
        self.trade_data[trade_id].settled = True

    def is_settled(self, trade_id):
        return True  # Placeholder for actual implementation

    def write_trades_to_file(self, file_name):
        with open(file_name, 'w') as file:
            for trade_info in self.trade_data:
                if trade_info!=None:
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

        # def get_ticker(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.ticker
        #     else:
        #         return None

        # def get_timestamp(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.timestamp
        #     else:
        #         return None

        # def get_price(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.price
        #     else:
        #         return None

        # def get_volume(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.volume
        #     else:
        #         return None

        # def get_buyer_mpid(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.buyer_mpid
        #     else:
        #         return None

        # def get_buyer_order_id(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.buyer_order_id
        #     else:
        #         return None

        # def get_seller_mpid(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.seller_mpid
        #     else:
        #         return None

        # def get_seller_order_id(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.seller_order_id
        #     else:
        #         return None

        # def get_trade_id(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].trade.trade_id
        #     else:
        #         return None
        
        # def get_buy_turn(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].buy_turn
        #     else:
        #         return None
            
        # def get_sell_turn(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].sell_turn
        #     else:
        #         return None
            
        # def get_settled(self, index):
        #     if 0 <= index <= self.trade_id_count:
        #         return self.trade_data[index].settled
        #     else:
        #         return None

#testing
if __name__ == "__main__":
    trade_processor = TradeProcessing()
    trade_processor.read_previous_trades_txt("testin.txt")
    trade_processor.read_new_trades(TradeMessage(ticker='TPCF0817', timestamp=8, price=100, volume=90, buyer_mpid='MPID1', buyer_order_id='None', seller_mpid='None', seller_order_id='0000000003', trade_id='4'))
    trade_processor.read_new_trades(TradeMessage(ticker='TPCF0521', timestamp=5, price=95, volume=100, buyer_mpid='MPID1', buyer_order_id='None', seller_mpid='None', seller_order_id='0000000003', trade_id='6'))
    trade_processor.read_new_trades(TradeMessage(ticker='TPCF1028', timestamp=10, price=105, volume=110, buyer_mpid='MPID1', buyer_order_id='None', seller_mpid='None', seller_order_id='0000000003', trade_id='7'))
    trade_processor.write_trades_to_file("testout.txt")


# import ast 

# class TradeMessage:
#     def __init__(self, ticker, timestamp, price, volume, buyer_mpid, buyer_order_id, seller_mpid, seller_order_id, trade_id):
#         self.ticker = ticker
#         self.timestamp = timestamp
#         self.price = price
#         self.volume = volume
#         self.buyer_mpid = buyer_mpid
#         self.buyer_order_id = buyer_order_id
#         self.seller_mpid = seller_mpid
#         self.seller_order_id = seller_order_id
#         self.trade_id = trade_id

#     def get_volume(self):
#         return self.volume
    
#     def get_price(self):
#         return self.price
    
#     def get_trade_id(self):
#         return self.trade_id
    
#     def get_buyer_mpid(self):
#         return self.buyer_mpid


# class TradeProcessing:
#     def __init__(self):
#         self.trade_data = []
#     def __read_trades_txt(self, file):
#         with open(file, 'r') as file:
#             for line in file:
#                 trade_data_str = line.strip().replace("TradeMessage(", "").replace(")", "")
#                 # Enclose attribute names in quotes to make it a valid dictionary string
#                 trade_data_str = trade_data_str.replace('ticker=', '"ticker":').replace('timestamp=', '"timestamp":').replace('price=', '"price":').replace('volume=', '"volume":').replace('buyer_mpid=', '"buyer_mpid":').replace('buyer_order_id=', '"buyer_order_id":').replace('seller_mpid=', '"seller_mpid":').replace('seller_order_id=', '"seller_order_id":').replace('trade_id=', '"trade_id":')
#                 trade_data = ast.literal_eval("{" + trade_data_str + "}")

#                 ticker = trade_data.get('ticker')
#                 timestamp = int(trade_data.get('timestamp'))
#                 price = int(trade_data.get('price'))
#                 volume = int(trade_data.get('volume'))
#                 buyer_mpid = trade_data.get('buyer_mpid')
#                 buyer_order_id = trade_data.get('buyer_order_id')
#                 seller_mpid = trade_data.get('seller_mpid')
#                 seller_order_id = trade_data.get('seller_order_id')
#                 trade_id = trade_data.get('trade_id')

#                 # Create TradeMessage object
#                 trade = TradeMessage(ticker, timestamp, price, volume, buyer_mpid, buyer_order_id, seller_mpid, seller_order_id, trade_id)
#                 buy_turn = int(ticker[4:6])
#                 sell_turn = int(ticker[-2:])
#                 settled = False #self.is_settled(trade_id)
#                 self.trade_data.append([trade, buy_turn, sell_turn, settled])

#     def read_trades_txt(self, infile, pasttradefile):
#         self.__read_trades_txt(pasttradefile)
#         self.__read_trades_txt(infile)
#         return self.trade_data

#     def get_trades(self):
#         return self.trade_data

#     def set_to_settled(self, trade_id):
#         for trade_info in self.trade_data:
#             if (trade_info[0].get_trade_id() == trade_id):
#                 trade_info[3] = True
#                 break

#     def write_trades_to_file(self, file_name):
#         with open(file_name, 'w') as file:
#             for trade_info in self.trade_data:
#                 trade = trade_info[0]
#                 ticker = trade.ticker
#                 timestamp = trade.timestamp
#                 price = trade.price
#                 volume = trade.volume
#                 buyer_mpid = trade.buyer_mpid
#                 buyer_order_id = trade.buyer_order_id
#                 seller_mpid = trade.seller_mpid
#                 seller_order_id = trade.seller_order_id
#                 trade_id = trade.trade_id
        
#                 trade_str = f"TradeMessage(ticker='{ticker}', timestamp={timestamp}, price={price}, volume={volume}, buyer_mpid='{buyer_mpid}', buyer_order_id='{buyer_order_id}', seller_mpid='{seller_mpid}', seller_order_id='{seller_order_id}', trade_id='{trade_id}')\n"
#                 file.write(trade_str)
#             self.trade_data.clear()


# #testing
# if __name__ == "__main__":
#     trade_processor = TradeProcessing()
#     trade_processor.read_trades_txt("testin.txt","testout.txt")
#     trade_processor.write_trades_to_file("testout.txt")
#     trade_processor.read_trades_txt("testin2.txt","testout.txt")
#     trade_processor.write_trades_to_file("testout.txt")