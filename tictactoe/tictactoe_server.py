import tictactoe
import argparse
import random
import socket
import sys


##
# Initialize globals.
game = tictactoe.TicTacToe()


##
# Parse command-line arguments.
parser = argparse.ArgumentParser()
parser.add_argument('-n', dest='hostname', default='localhost')
parser.add_argument('-p', dest='port', default=random.randint(40000, 50000))
args = parser.parse_args()


##
# Bind to port and listen.
server = socket.socket()
server.bind( (args.hostname, args.port) )
server.listen()

print(f'Server bound to and listening on ({args.hostname}, {args.port})')


##
# Accept incoming connections.
def read_client(the_client: socket.socket) -> str:
    res = str()
    while True:
        data = the_client.recv(64)
        if not data:
            break
        res += data.decode('utf-8')
    res = res.rstrip()
    return res


while True:
    client, addr = server.accept()
    client.settimeout(10)
    response = str()

    print('client connected at', addr)


    # Read a split response from client, throw exception if it takes too long.
    try:
        response = read_client(client)
        response = response.split(',')
    except socket.timeout:
        print(f'{addr} timed out.')
        continue
    

    # Parse client request.
    try:
        row = int(response[0].strip())
        col = int(response[1].strip())
        game.move(row, col)
    except ValueError:
        pass
    except IndexError:
        pass


    # Send msg to client.
    msg = str(game)
    client.send(msg.encode('utf-8'))


    client.close()


##
# Close server.
server.close()