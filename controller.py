
from client import *
from command import *

class Controller:
    # evaliation framework
    # read operations from a file, and then send 1) makekey/makenode to dht and/or 2) lookup request to client

    def __init__(self, logfile, dht):
        self.cmds = parse(logfile)
        self.clients = []
        self.dht = dht
        self.length_log = len(self.cmds)
    
    def execute(self):
        cmd = self.cmds.pop(0)
        print(cmd)
        if cmd.type == "MakeKey":
            key, val = cmd.key, cmd.val
            self.dht.DHTMakeKey(key, val)

        if cmd.type == "MakeNode":
            key, val = cmd.key, cmd.val
            self.dht.DHTMakeNode(key, val)

        if cmd.type == "ClientLookUp":
            local_node = self.dht.nodes[cmd.local_node_id]
            key = cmd.dest_key
            lookup_id = cmd.lookup_id
            client = Client(local_node, key, lookup_id)
            client.make_query()
            self.clients.append(client)

        # if cmd.type == "Finish":
        #     self.dht.clean_up()

        

def parse(logfile):
    commands = []
    f2 = open(logfile, 'r')
    logs = f2.readlines()
    f2.close()
    for line in logs:
        if "make key" in line:
            id = line[-22:-12]
            val = line[-11:-1]
            commands.append(MakeKey(id,val))
        if "make node" in line:
            id = line[-22:-12]
            val = line[-11:-1]
            commands.append(MakeNode(id, val))
        if "look up" in line:
            req_node = line[-22:-12]
            dest = line[-11:-1]
            linenum = line.split(":")[0]
            commands.append(ClientLookUp("L{}".format(linenum), req_node, dest))
    commands.append(Finish())
    return commands

# if __name__ == '__main__':
#     testfile = 'log.txt'
#     keyvalfile = 'keyval.txt'
#     commands = parse(testfile, keyvalfile)
#     for command in commands:
#         print(command)
