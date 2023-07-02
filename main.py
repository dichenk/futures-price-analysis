from binance import ThreadedWebsocketManager
from threading import Thread
import time as tm
import pandas as pd
import json


class Stream:

    def get_data(self, var):
        if 'data' in var:
            self.read_data(var['data'])
        else:
            self.stream_error = True
 
    def read_data(self, data): 
        coin = data['s']
        price = float(data['a'])
        time_check = data['T']//1000  # don't need milliseconds   

        if self.prev_price[coin] is None:
            self.prev_price[coin] = price
            return

        change_price = (price / self.prev_price[coin] - 1) * 100

        if change_price:
            print(coin, price, self.prev_price[coin], f'{change_price:.4f}')

        self.prev_price[coin] = price 

        #     '''add data to the df's up'''
        #     future_data[coin].loc[-1] = {
        #         'time_fix': time_check, 
        #         'price': price, 
        #         'prev_price': last_price[coin], 
        #         'diff': diff
        #     }
        #     future_data[coin].index += 1
        #     future_data[coin] = future_data[coin].sort_index()

        #     last_price[coin] = price

        #     future_data[coin].to_csv(f'{coin}.csv')


    def start(self):
        self.bsm = ThreadedWebsocketManager()
        self.bsm.start()
        self.stream_error = False
        self.streams = ['btcusdt@bookTicker', 'ethusdt@bookTicker']
        self.symbols = ['BTCUSDT', 'ETHUSDT']
        self.prev_price = {
            'BTCUSDT': None,
            'ETHUSDT': None
        }

        # output to the trade_history
        self.stream = self.bsm.start_futures_multiplex_socket(callback=stream.get_data, streams=self.streams)# symbol=self.symbols[0])

        # monitoring the error
        restart_stream = Thread(target=stream.restart_stream, daemon=True)
        restart_stream.start()
    
    def restart_stream(self):
        while 1:
            tm.sleep(1)
            if self.stream_error == True:
                self.bsm.stop_socket(self.stream)
                tm.sleep(5)
                self.stream_error = False
                self.stream = self.bsm.start_futures_multiplex_socket(callback=stream.get_data, streams=self.streams)#symbol=self.symbols[0])
            

stream = Stream()
stream.start()
stream.bsm.join()



# '''futures info'''
# df = pd.DataFrame(columns=['time_fix', 'price', 'prev_price', 'diff'])

# future_data = dict()
# future_data['BTCUSDT'] = df
# future_data['ETHUSDT'] = df.copy()