import threading
import websocket
import json
import requests


class WebSockInterface:
    def __init__(self, key, secret):
        super().__init__()
        uri = 'wss://api.bitfinex.com/ws/2'
        self.sock = SockThread(uri)

    def wait_for_connection(self):
        while not self.sock.is_connected():
            pass

    def disconnect(self):
        self.sock.disconnect()
        self.sock.join()

    def send_ping(self):
        self.sock.send_msg({'event': 'ping'})

    def subscribe_ticker(self, symbol):
        self.sock.send_msg({'event': 'subscribe',
                            'channel': 'ticker',
                            'symbol': symbol})

    def subscribe_trades(self, symbol):
        self.sock.send_msg({'event': 'subscribe',
                            'channel': 'trades',
                            'symbol': symbol})

    def subscribe_books(self, symbol, precision, frequency, length):
        self.sock.send_msg({'event': 'subscribe',
                            'channel': 'book',
                            'symbol': symbol,
                            'prec': precision,
                            'freq': frequency,
                            'len': length})

    def subscribe_raw_books(self, symbol, length):
        self.sock.send_msg({'event': 'subscribe',
                            'channel': 'book',
                            'symbol': symbol,
                            'prec': 'R0',
                            'len': length})

    def subscribe_candles(self):
        self.sock.send_msg({'event': 'subscribe',
                            'channel': 'candles',
                            'key': 'trade:1m:tBTCUSD'})



    def list_symbols(self):
        return requests.get('https://api.bitfinex.com/v1/symbols_details').json()


class SockThread(threading.Thread):
    def __init__(self, uri):
        super().__init__()
        self.uri = uri
        self.sock_app = websocket.WebSocketApp(url=self.uri,
                                               on_message=self.on_msg,
                                               on_close=self.on_close,
                                               on_error=self.on_error,)
        self.sock_connected = False
        self.start()

    def is_connected(self):
        return self.sock_connected

    def disconnect(self):
        self.sock_app.close()

    def send_msg(self, msg):
        self.sock_app.send(json.dumps(msg))

    def on_error(self, ws, msg):
        print('error')
        print(msg)

    def on_msg(self, ws, message):
        msg = json.loads(message)
        if 'event' in msg:
            if msg['event'] == 'info' and msg['version'] == 2:
                self.sock_connected = True
            elif msg['event'] == 'pong':
                print(message)
            elif msg['event'] == 'subscribed':
                if msg['channel'] == 'ticker':
                    pass
                elif msg['channel'] == 'trades':
                    pass
                elif msg['channel'] == 'book':
                    pass
                elif msg['channel'] == 'candles':
                    pass
                else:
                    print(message)
                    raise ValueError('unhandled subscription')
            else:
                print(message)
                raise ValueError('unhandled event')
        else:
            if type(msg) == list:
                if 'hb' in msg:
                    pass
                elif 'te' in msg or 'tu' in msg:
                    print(msg)
                else:
                    if type(msg[1]) == list and \
                            (type(msg[1][0]) == float or type(msg[1][0]) == int):
                        print(msg)
                    elif type(msg[1]) == list and type(msg[1][0]) == list:
                        print(msg)
                    else:
                        print(message)
                        raise ValueError('message not recognized')
            else:
                print(message)
                raise ValueError('unhandled message type')

    def on_close(self, ws):
        self.sock_connected = False
        print('closing')

    def run(self):
        self.sock_app.run_forever()
        self.sock_connected = False

