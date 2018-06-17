from binance_db.candle import Candle
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class BinanceDB():
    def __init__(self, password, user='binancedb', url='postgres', port=5432, db='binancedb', echo=False):
        conn = 'postgresql://{}:{}@{}:{}/{}'.format(
            user, password, url, port, db)

        self.engine = create_engine(conn, echo=echo)
        Candle.metadata.create_all(self.engine)

    def get_session(self):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        return Session()
