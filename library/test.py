from ezmpncgame import EZMPNCApplication
from game import Game
import sys
import argparse
import random
# Initialize game server with hostname, port parameters from command line.

# Pass game instance to ezmpnc game.

if __name__=='__main__':
    app = EZMPNCApplication(sys.argv, Game())
    sys.exit(app.exec_())