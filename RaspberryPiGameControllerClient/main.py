from RasPiGameControllerClient import RasPiGameControllerClient
# You should change ip and port for your own raspberry pi
RC = RasPiGameControllerClient('192.168.43.15', 16666)
RC.run()
