


import bitfinex
import time
from pymongo import MongoClient
import json


db_client = MongoClient()


ws = bitfinex.WebSockInterface(key='tYuC4AIUmYN0u9oSJqgTXLfDYtI0w8TTZgXocgSRJgn',
                               secret='F75ZRJRUZM2ZmTRKV6LJVcVlUzGP2icJAbzPYDaVJfb')
ws.wait_for_connection()

ws.subscribe_ticker('tBTCUSD')

# ws.subscribe_trades('tBTCUSD')

# ws.subscribe_books('tBTCUSD', 'P0', 'F0', '25')

# ws.subscribe_raw_books('tBTCUSD', '25')

# ws.subscribe_candles()
# ws.authenticate()

time.sleep(10)
ws.disconnect()

