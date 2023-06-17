from time import sleep, time
from binance import ThreadedWebsocketManager  # gonna using the Binance WebSocket
import pandas as pd


start = time()

df = pd.DataFrame(columns=['price'])
'''variables for info about futures'''
future_data = {'error':False, 'ETHUSDT': df, 'BTCUSDT': df.copy()}
streams = ['ethusdt@bookTicker', 'btcusdt@bookTicker']

def trade_history(msg):
    '''define how to process incoming WebSocket messages
    an example of message: 
        {'stream': 'ethusdt@bookTicker', 'data': {
            'e': 'bookTicker', 
            'u': 2958234026278, 
            's': 'ETHUSDT', 
            'b': '1728.29',  # the best bid price for the trading pair
            'B': '124.718', 
            'a': '1728.30',  # the best ask price for the trading pair
            'A': '60.316', 
            'T': 1687038775261, # a timestamp for when the data was captured
            'E': 1687038775266
        }}
    '''
    if msg.get('e'):
        future_data['error'] = True
    else:
        coin = msg['data']['s']
        price = msg['data']['a']
        time = msg['data']['T']
        time_str = str(time)
        future_data[coin].loc[time_str] = [price]
    sleep(0.10)

'''to initialize the socket manager'''
bsm = ThreadedWebsocketManager()
bsm.start()

'''output to the trade_history'''
bsm.start_futures_multiplex_socket(callback=trade_history, streams=streams)


while 1:
    if time() - start > 30:
        break

'''stop websocket'''
bsm.stop()

future_data['ETHUSDT'].to_csv('eth.csv')
future_data['BTCUSDT'].to_csv('btc.csv')


