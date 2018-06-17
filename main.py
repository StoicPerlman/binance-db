import os
import time
from binance_db.db import BinanceDB
from binance_db.util.logger import Logger
from binance_db.candle import Candle, WSCandle
import binance_db.util.constants.ws as ws

from binance.client import Client
from binance.websockets import BinanceSocketManager

logger = Logger()
logger.info("Starting binance db...")

PAIR = os.environ['PAIR']
INTERVAL = '1m'

init = False
init_candles = []

def main():
    db = connect_db()
    client = Client(api_key='', api_secret='')
    bm = BinanceSocketManager(client)

    start_ws(db, bm)
    load_historical(db, client)
    logger.info("Binance DB locked and loaded!")

def connect_db():
    pgurl = os.environ['BDB_POSTGRES_URL']
    pgport = os.environ['BDB_POSTGRES_PORT']
    pguser = os.environ['BDB_POSTGRES_USER']
    pgpass = os.environ['BDB_POSTGRES_PASS']
    conn = f'postgresql://{pguser}:{pgpass}@{pgurl}:{pgport}/{pguser}'

    # let pg start up. first run can take longer than others
    logger.info("Waiting for Postgres...")
    pg_try = 0
    while True:
        time.sleep(5)
        try:
            bdb = BinanceDB(conn)
            break
        except:
            pg_try += 1
            if pg_try > 5:
                logger.error("Unable to connect to postgres")
                exit(1)

    return bdb.get_session()

def start_ws(db, bm):
    logger.info("Starting Binance WS...")
    pws = lambda x: process_ws(x, db)
    bm.start_kline_socket(PAIR, pws, interval=INTERVAL)
    bm.start()

def process_ws(msg, db):
    if msg[ws.EVENT_TYPE] == ws.ERROR_EVENT:
        logger.error(msg)
        exit(1)

    candle = WSCandle(msg)

    if candle.closed:
        global init
        logger.info(f'New candle: {candle}')
        if init:
            db.add(candle)
            db.commit()
        else:
            init_candles.append(candle)

def load_historical(db, client):
    logger.info("Getting historical data...")

    # if db already has data start there
    newest_candle = get_newest_in_db(db)
    if newest_candle != None:
        starttime = str(newest_candle.close_time)
    else:
        starttime = '100 years ago UTC'
        logger.info("No data in DB. Getting all history...")
        logger.info("This could take a while...")

    klines = client.get_historical_klines(PAIR, INTERVAL, starttime)
    logger.info("Data retrieved, adding to db...")

    # last kline not closed will get from ws
    klines = klines[:-1]

    for b in batch(klines, 1000):
        for kline in b:
            candle = Candle(PAIR, kline)

            # long running imports can cause overlap
            if candle not in init_candles:
                db.add(candle)
        db.commit()

    global init
    init = True
    db.add_all(init_candles)
    db.commit()
    logger.info("Historical data loaded...")

def get_newest_in_db(db):
    newest = db.query(Candle).filter_by(pair=PAIR).order_by(Candle.close_time.desc()).first()
    logger.info(f'Most recrent candle on start: {newest}')
    return newest

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

if __name__ == '__main__':
    main()
