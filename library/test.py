from ezmpncgame import EZMPNCApplication
from game import Game
import sys

if __name__=='__main__':
    app = EZMPNCApplication(sys.argv, Game())
    sys.exit(app.exec_())