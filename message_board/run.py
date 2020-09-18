import messageboard
import ezmpncgame
import sys

if __name__=='__main__':
    app = messageboard.MessageBoard()
    server = ezmpncgame.EZMPNCServer(app)
    sys.exit(server.exec_())