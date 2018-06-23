from datetime import datetime
import binance_db.util.constants.ws as ws
import binance_db.util.constants.rest as rest
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime, Index

Base = declarative_base()

class Candle(Base):
    __tablename__ = 'candles'

    pair = Column(String, primary_key=True)
    open_time = Column(DateTime, primary_key=True)
    close_time = Column(DateTime)
    open_price = Column(Float)
    close_price = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    qav = Column(Float)
    trades = Column(Integer)
    tbbav = Column(Float)
    tbqav = Column(Float)

    __table_args__ = (
        Index('open_time_asc', open_time.asc(), postgresql_using='btree'),
        Index('open_time_desc', open_time.desc(), postgresql_using='btree'),
    )

    def __init__(self, pair, kline):
        self.pair = pair
        self.open_time = self.to_date(kline[rest.OPEN_TIME])
        self.close_time = self.to_date(kline[rest.CLOSE_TIME])
        self.open_price = float(kline[rest.OPEN_PRICE])
        self.close_price = float(kline[rest.CLOSE_PRICE])
        self.high = float(kline[rest.HIGH])
        self.low = float(kline[rest.LOW])
        self.volume = float(kline[rest.VOLUME])
        self.qav = float(kline[rest.QAV])
        self.trades = kline[rest.TRADES]
        self.tbbav = float(kline[rest.TBBAV])
        self.tbqav = float(kline[rest.TBQAV])

    def __eq__(self, other):
        if other == None:
            return False
        return self.pair == other.pair and self.close_time == other.close_time

    def __repr__(self):
        date = self.open_time.strftime('%Y-%m-%d %H:%M:%S')
        return "<Candle(pair={}, open_time={}, open={}, close={})>".format(
                self.pair, date, self.open_price, self.close_price)

    @staticmethod
    def to_date(timestamp):
        return datetime.utcfromtimestamp(timestamp / 1000)

class WSCandle(Candle):
    def __init__(self, ws_event):
        self.pair = ws_event[ws.SYMBOL]
        self.open_time = self.to_date(ws_event[ws.KLINE_DATA][ws.OPEN_TIME])
        self.close_time = self.to_date(ws_event[ws.KLINE_DATA][ws.CLOSE_TIME])
        self.open_price = float(ws_event[ws.KLINE_DATA][ws.OPEN_PRICE])
        self.close_price = float(ws_event[ws.KLINE_DATA][ws.CLOSE_PRICE])
        self.high = float(ws_event[ws.KLINE_DATA][ws.HIGH_PRICE])
        self.low = float(ws_event[ws.KLINE_DATA][ws.LOW_PRICE])
        self.volume = float(ws_event[ws.KLINE_DATA][ws.VOLUME])
        self.qav = float(ws_event[ws.KLINE_DATA][ws.QAV])
        self.trades = ws_event[ws.KLINE_DATA][ws.TRADES]
        self.tbbav = float(ws_event[ws.KLINE_DATA][ws.TBBAV])
        self.tbqav = float(ws_event[ws.KLINE_DATA][ws.TBQAV])
        self.closed = ws_event[ws.KLINE_DATA][ws.IS_CLOSED]
