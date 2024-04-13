from command import *
from DHT import *
from controller import *


logfile = 'log.txt'
keyvalfile = 'keyval.txt'
dht = DHT()
controller = Controller(logfile, dht)
for i in range(controller.length_log):
    controller.execute()