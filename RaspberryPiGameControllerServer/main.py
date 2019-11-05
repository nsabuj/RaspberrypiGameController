from RasPiGameControllerServer import RasPiGameControllerServer
# You should change ip and port for your own raspberry pi
RC = RasPiGameControllerServer('192.168.1.126',16666)
RC.run()