import selectors
import socket
import threading
from time import sleep
from lib.libclient import iMessage


class RasPiGameControllerClient:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.addr = (ip, port)
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket()

    def _get_sense_forever(self,socket):
        try:
            while True:
                sleep(0.15)
                self.sock.send("get".encode('utf-8'))
        except KeyboardInterrupt:
            print("caught keyboard interrupt, exiting")
        finally:
            self.sel.close()
            self.sock.close()

    def run(self):
        self.sock.connect(self.addr)
        self.sock.setblocking(False)
        message = iMessage(self.sel, self.sock, self.addr)
        self.sel.register(self.sock, selectors.EVENT_READ, data=message)
        threading.Thread(target=self._get_sense_forever, args=(self.sock,)).start()
        while True:
            events = self.sel.select(timeout=1)
            for key, mask in events:
                callback = key.data
                callback.process_events(mask)
