from time import sleep
from binance import ThreadedWebsocketManager  # gonna using the Binance WebSocket
import pandas as pd


'''variables for info about futures'''
eth_data = {'error':False}
btc_data = {'error':False}
streams = ['ethusdt@bookTicker', 'btcusdt@bookTicker']

def trade_history(msg):
    '''define how to process incoming WebSocket messages'''
    print(msg)
    sleep(0.10)

'''to initialize the socket manager'''
bsm = ThreadedWebsocketManager()
bsm.start()

'''output to the trade_history'''
bsm.start_futures_multiplex_socket(callback=trade_history, streams=streams)


while 1:
    pass

'''stop websocket'''
bsm.stop()

