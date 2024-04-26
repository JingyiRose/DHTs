
from client import *
from command import *

class Controller:
    # evaluation framework
    # read operations from a file, and then send 1) makekey/makenode to dht and/or 2) lookup request to client

    def __init__(self, commandfile, dht, rep_filename = None, is_cheating = False):
        # turning on "cheat" (by setting it to true) lets dht calls self.cheat() after all keys/nodes are inserted 

        self.cmds = parse_commands(commandfile)
        self.clients = []
        self.dht = dht
        self.dht.is_cheating = is_cheating
        self.length_log = len(self.cmds)
        if os.path.exists(rep_filename):
            os.remove(rep_filename)
        self.rep_filename = rep_filename

        self.is_cheating = is_cheating
        self.lookup_started = False
        
    
    def execute(self):
        for cmd in self.cmds:
            if cmd.type == "InsertKey":
                key, val = cmd.key, cmd.val
                self.dht.InsertKey(key, val)

            if cmd.type == "MakeNode":
                id, ip, port = cmd.id, cmd.ip, cmd.port
                self.dht.MakeNode(id, ip, port)

            if cmd.type == "ClientLookUp":
                if self.is_cheating:
                    if not self.lookup_started:
                        self.dht.cheat()
                        self.lookup_started = True
            
                local_node = self.dht.nodes[cmd.local_node_id]
                query_key = cmd.destination_key
                client = Client(local_node, query_key, write_to = self.rep_filename)
                client.make_query()
                self.clients.append(client)

        # if cmd.type == "Finish":
        #     self.dht.clean_up()



# if __name__ == '__main__':
#     testfile = 'log.txt'
#     keyvalfile = 'keyval.txt'
#     commands = parse(testfile, keyvalfile)
#     for command in commands:
#         print(command)
