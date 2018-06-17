# Binance DB

A local cache for Binance data, stored in Postgres

## Setup

### Server

On the server you wish to run the Postgres DB on.

```bash
git clone https://github.com/StoicPerlman/binance-db.git
export BDB_POSTGRES_PASS=supersecret
docker-compose up -d
```

This will pull all available 1 minute candles from Binance and store them in a Postgres DB container. This container has a persistant volume configured for the data, meaning it can be deleted and restarted as much as you want.

When started it will check if there is any existing data in the DB. If not it will fetch all. This takes less than 15 mintes and takes up about 250 MB at the time of this writing. If there is existing data it will pull just the data starting from the newest entry in the DB.

A thread is started and connected to the Binance web socket. This will add new data as it is available. If you do not want continuously updating data you can run both containers then just kill the binance-db one.

### Client

You can pip install this package to connect to DB and have a sqlalchemy session started for use in your own app.

```bash
pip3 install binance-db
```

```python
# if you did not override any settings on the server 
# all you have to supply is url and password
from binance_db.db import BinanceDB
from binance_db.candle import Candle

bdb = BinanceDB(user=pguser, password=pgpass, url=pgurl, port=pgport, db=pgdb)

# this is a normal sqlalchemy session
# see binance_db.candle.Candle for schema
db = bdb.get_session()

new = db.query(Candle).filter_by(pair='BTCUSDT').order_by(Candle.close_time.desc()).first()

print(new.pair)
print(new.open_time)
print(new.close_time)
print(new.open_price)
print(new.close_price)
print(new.high)
print(new.low)
print(new.volume)
print(new.qav) # Quote asset volume
print(new.trades) # Number of trades
print(new.tbbav) # Taker buy base asset volume
print(new.tbqav) # Taker buy quote asset volume
```
