
from client import *
from command import *

class Controller:
    # evaluation framework
    # read operations from a file, and then send 1) makekey/makenode to dht and/or 2) lookup request to client

    def __init__(self, commandfile, dht, rep_filename = None):
        self.cmds = parse_commands(commandfile)
        self.clients = []
        self.dht = dht
        self.length_log = len(self.cmds)
        if os.path.exists(rep_filename):
            os.remove(rep_filename)
        self.rep_filename = rep_filename
    
    def execute(self):
        for cmd in self.cmds:
            if cmd.type == "InsertKey":
                key, val = cmd.key, cmd.val
                self.dht.InsertKey(key, val)

            if cmd.type == "MakeNode":
                id, ip, port = cmd.id, cmd.ip, cmd.port
                self.dht.MakeNode(id, ip, port)

            if cmd.type == "ClientLookUp":
                local_node = self.dht.nodes[cmd.local_node_id]
                query_key = cmd.destination_key
                client = Client(local_node, query_key, write_to = self.rep_filename)
                client.make_query()
                self.clients.append(client)

        # if cmd.type == "Finish":
        #     self.dht.clean_up()

        

# def parse(logfile):
#     commands = []
#     f2 = open(logfile, 'r')
#     logs = f2.readlines()
#     f2.close()
#     for line in logs:
#         if "make key" in line:
#             id = line[-22:-12]
#             val = line[-11:-1]
#             commands.append(MakeKey(id,val))
#         if "make node" in line:
#             id = line[-22:-12]
#             val = line[-11:-1]
#             commands.append(MakeNode(id, val))
#         if "look up" in line:
#             req_node = line[-22:-12]
#             dest = line[-11:-1]
#             linenum = line.split(":")[0]
#             commands.append(ClientLookUp("L{}".format(linenum), req_node, dest))
#     commands.append(Finish())
#     return commands

# if __name__ == '__main__':
#     testfile = 'log.txt'
#     keyvalfile = 'keyval.txt'
#     commands = parse(testfile, keyvalfile)
#     for command in commands:
#         print(command)
