"""
    Python lookalike for the netcat tool.
"""
import argparse

import sys
import socket


BUFFER_SIZE = 1024


class Listener(object):

    def __init__(self, port):
        self.port = port

    def start(self):
        listeningSocket = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_IP)
        listeningSocket.bind(('127.0.0.1', self.port))
        listeningSocket.listen(1)
        clientSock, clientAddr = listeningSocket.accept()

        try:
            while True:
                buf = clientSock.recv(BUFFER_SIZE)
                if buf == '':
                    break
                sys.stdout.write(buf)
        finally:
            clientSock.close()
            if listeningSocket:
                listeningSocket.close()


class Connector(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        serverSocket = socket.create_connection((self.host, self.port))
        try:
            while True:
                # TODO: this seems to block longer than needed
                data = sys.stdin.read(BUFFER_SIZE)
                if not data:
                    break
                serverSocket.send(data)
        finally:
            serverSocket.close()


def main():
    argsparser = argparse.ArgumentParser()
    argsparser.add_argument("-l", "--listen", action='store_true', default=False, help="listen mode")
    argsparser.add_argument("-p", "--port", type=int, help="listen on port")
    options, remaining = argsparser.parse_known_args(sys.argv[1:])

    if options.listen:
        Listener(options.port).start()
    else:
        host = str(remaining[0])
        port = int(remaining[1])
        Connector(host, port).connect()
    return 0

if __name__ == "__main__":
    sys.exit(main())
