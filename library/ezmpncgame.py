import argparse
import socket
import random

def debug_print(fn):
    def wrapper(*args, **kwargs):
        print('Entered', fn.__name__, 'with args', *args, 'and kwargs', **kwargs)
        ret = fn(*args, **kwargs)
        print('Exited', fn.__name__)
        return ret
    return wrapper

def catch_interrupt(fn):
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyboardInterrupt:
            return 1
    wrapper.__name__ = f'catch-{fn.__name__}'
    return wrapper

class EZMPNCApplication:

    @debug_print
    def parse_args(args: list) -> argparse.Namespace:
        parser = argparse.ArgumentParser()
        parser.add_argument('-n', dest='hostname', default='127.0.0.1')
        parser.add_argument('-p', dest='port', default=random.randint(40000, 50000), type=int)
        return parser.parse_args(args[1:])

    @debug_print
    def read_socket(sock: socket.socket) -> str:
        res = str()
        while True:
            raw_data = sock.recv(64)
            if not raw_data: break
            res += raw_data.decode('utf-8').rstrip()
        return res
    
    @debug_print
    def __init__(self, args, game) -> None:
        self.server = socket.socket()
        self.args = EZMPNCApplication.parse_args(args)
        self.game = game

    @debug_print
    def __del__(self):
        if self.server:
            self.server.close()
    
    @debug_print
    @catch_interrupt
    def exec_(self) -> int:
        self.server.bind( (self.args.hostname, self.args.port) )
        self.server.listen()
        print('INFO:', f'Server listening on ({self.args.hostname}, {self.args.port})')
        while self.server:
            client, address = self.server.accept()
            request = EZMPNCApplication.read_socket(client)
            response = self.game.process_request(request)
            client.send(response.encode('utf-8'))
            client.close()
        return 0