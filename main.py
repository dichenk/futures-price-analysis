from binance import ThreadedWebsocketManager
from threading import Thread
import time as tm
import db_func

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
            db_func.write_data(coin, price, time_check, 0)
            return

        change_price = (price / self.prev_price[coin] - 1) * 100

        if abs(change_price) > 0.001:
            db_func.write_data(coin, price, time_check, change_price)

        self.prev_price[coin] = price

        a = db_func.check_prices()
        if int(tm.time()) % 10 == 0:
            self.b = 1
        if self.b == 1 and int(tm.time()) % 10 == 1: 
            print(a[0] - a[1])
            self.b = 0

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
        self.b = 0  # variable for limit printing

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