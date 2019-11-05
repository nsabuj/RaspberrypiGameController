import selectors
import socket
from lib.libserver import SenseData


class RasPiGameControllerServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (ip, port)
        self.sd = SenseData()
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket()

    def _accept(self, sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self._read)

    def _read(self, conn, mask):
        try:
            data = conn.recv(1000)  # Should be ready
            if data:
                res = self.sd.build()
                print(res)
                conn.send(res)  # Hope it won't block
            else:
                print('closing', conn)
                self.sel.unregister(conn)
                conn.close()
        except:
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()

    def run(self):
        self.sock.bind(self.addr)
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self._accept)
        while True:
            events = self.sel.select()
            for key, mask in events:
                imessage = key.data
                imessage(key.fileobj, mask)
