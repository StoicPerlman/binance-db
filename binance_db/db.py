from binance_db.candle import Candle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class BinanceDB():
    def __init__(self, connstr, echo=False):
        self.engine = create_engine(connstr, echo=echo)
        Candle.metadata.create_all(self.engine)

    def get_session(self):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        return Session()
