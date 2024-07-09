"""
TCP SERVER ECHO

nohup python3 test/tcp_server.py &
netstat -tlnp | grep 31702
"""

import json
import socketserver


class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        while True:
            data = self.request.recv(1024).strip()
            if not data:
                print('close by peer')
                break
            # echo
            self.request.sendall(data)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 31703
    # Create the server, binding to localhost on port 9999
    with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()
