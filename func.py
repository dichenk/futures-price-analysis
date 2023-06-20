import time as tm
import pandas as pd
import time

'''futures info'''
future_data = {
    'error':False,
    'ETHUSDT': None,
    'BTCUSDT': None
    }
streams = ['ethusdt@bookTicker', 'btcusdt@bookTicker']
# coins = {
#     'eth': 'ETHUSDT',
#     'btc': 'BTCUSDT'
#     }


def data_reset():
    df = pd.DataFrame(columns=['time', 'price'])
    future_data['ETHUSDT'] = df
    future_data['BTCUSDT'] = df.copy()

def analyse(var):
    data_reset()
    coin = var['data']['s']
    price = var['data']['a']
    time = var['data']['T']

    future_data[coin].loc[-1] = [time, price]
    future_data[coin].index += 1
    future_data[coin] = future_data[coin].sort_index()

    tm.sleep(.5)
    
    # a = tm.strftime('%X')
    # if a[3:5] == '02':
    print(future_data)



if __name__ == '__main__':
    analyse()