import csv
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

def read_trades_csv(file_name):
    past_trades = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader: #assuming this format, TradeMessage(ticker = 'TPCF0602', timestamp=4,price=100,volume=100,buyer_mpid='MPID1', seller_order_id='0000000003',trade_id='1')
            # Parse the string to extract TradeMessage attributes
            trade_data_str = row[0].strip().replace("TradeMessage(", "").replace(")", "")
            trade_data = ast.literal_eval("{" + trade_data_str + "}")
            
            # Extract attribute values
            ticker = trade_data.get('ticker')
            timestamp = int(trade_data.get('timestamp'))
            price = int(trade_data.get('price'))
            volume = int(trade_data.get('volume'))
            buyer_mpid = trade_data.get('buyer_mpid')
            buyer_order_id = trade_data.get('buyer_order_id')
            seller_mpid = trade_data.get('seller_mpid')
            seller_order_id = trade_data.get('seller_order_id')
            trade_id = trade_data.get('trade_id')

            trade = TradeMessage(ticker, timestamp, price, volume, buyer_mpid, buyer_order_id, seller_mpid, seller_order_id, trade_id)
            
            buy_turn = int(ticker[4:6])
            sell_turn = int(ticker[-2:])
            settled = is_settled(ticker) #placeholder for checking if trade is settled
            
            past_trades.append([trade, buy_turn, sell_turn, settled])
    return past_trades


def is_settled(ticker): #placeholder
    return True; 


def write_trades_to_file(trade_data, file_name):
    with open(file_name, 'w') as file:
        for trade_info in trade_data:
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
            
            # Format the trade message as a string
            trade_str = f"TradeMessage(ticker='{ticker}', timestamp={timestamp}, price={price}, volume={volume}, buyer_mpid='{buyer_mpid}', buyer_order_id='{buyer_order_id}', seller_mpid='{seller_mpid}', seller_order_id='{seller_order_id}', trade_id='{trade_id}')\n"
            
            file.write(trade_str)
