from binance import ThreadedWebsocketManager  # gonna using the Binance WebSocket
import func


def trade_history(msg):
    func.analyse(msg)

def main():

    '''to initialize the socket manager'''
    bsm = ThreadedWebsocketManager()
    bsm.start()

    # '''output to the trade_history'''
    # bsm.start_futures_multiplex_socket(callback=trade_history, streams=func.streams)
    for i in func.symbols:
        bsm.start_symbol_ticker_futures_socket(callback=trade_history, symbol=i)
            
    '''
    for keeping the ThreadedWebsocketManager running (join to the main thread)
    '''
    bsm.join()

main()