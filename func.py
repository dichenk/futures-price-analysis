import time as tm
import pandas as pd


def data_reset():
    df = pd.DataFrame(columns=['time', 'price', 'prev_price', 'diff'])
    future_data['ETHUSDT'] = df
    future_data['BTCUSDT'] = df.copy()

def analyse(var):
    coin = var['data']['s']
    price = var['data']['a']
    time = var['data']['T']
    
    if price != last_price[coin]:
        diff = float(price) / float(last_price[coin]) * 100 - 100  # in percent 

        future_data[coin].loc[-1] = [time, price, last_price[coin], diff]
        future_data[coin].index += 1
        future_data[coin] = future_data[coin].sort_index()

        future_data[coin].to_csv(f'{coin}.csv')

        last_price[coin] = price
        print(tm.strftime('%X'), coin, price, diff, 'процентов')
    tm.sleep(1)
    

'''futures info'''
future_data = {
    'error':False,
    'ETHUSDT': None,
    'BTCUSDT': None
    }
streams = ['ethusdt@bookTicker', 'btcusdt@bookTicker']
symbols = ['ETHUSDT', 'BTCUSDT']
last_price = {
    'ETHUSDT': -float('inf'),
    'BTCUSDT': -float('inf')
}
data_reset()

if __name__ == '__main__':
    data_reset()
    analyse()