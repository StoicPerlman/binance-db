from binance_db.db import BinanceDB
from binance_db.util.logger import Logger
from binance_db.candle import Candle, WSCandle
import binance_db.util.constants.ws as ws

from binance.client import Client
from binance.websockets import BinanceSocketManager

logger = Logger()

bdb = BinanceDB('sqlite:///:memory:', echo=True)
db = bdb.get_session()

client = Client(api_key='', api_secret='')
bm = BinanceSocketManager(client)

PAIR = 'BTCUSDT'
INTERVAL = '1m'

def main():
    pws = lambda x: process_ws(x, db)
    bm.start_kline_socket(PAIR, pws, interval=INTERVAL)
    bm.start()
    load_historical()

def process_ws(msg, db):
    if msg[ws.EVENT_TYPE] == ws.ERROR_EVENT:
        logger.error(msg)
        exit(1)

    candle = WSCandle(msg)

    if candle.closed:
        logger.debug(f'New candle: {candle}')
        db.add(candle)
        db.commit()

def load_historical():
    klines = client.get_historical_klines('BTCUSDT', '1m', '10 minutes ago UTC')

    # last isn't closed and will be added by ws
    klines = klines[:-1]
    candles = []

    for kline in klines:
        candles.append(Candle(PAIR, kline))

    db.add_all(candles)
    db.commit()

if __name__ == '__main__':
    main()
