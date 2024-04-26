# from env import *


class Command:
    # use for controller
    def __init__(self):
        self.type = None
    
class InsertKey(Command):
    def __init__(self, key, val):
        super().__init__()
        self.key = key
        self.val = val
        self.type = "InsertKey"
    
    def __str__(self) -> str:
        return "InsertKey(key={}, val={})".format(self.key, self.val)
    
class MakeNode(Command):
    def __init__(self, id, ip, port):
        super().__init__()
        self.id = id
        self.ip = ip
        self.port = port
        self.type = "MakeNode"
    
    def __str__(self) -> str:
        return "MakeNode(id={}, ip={}, port={})".format(self.id, self.ip, self.port)

class ClientLookUp(Command):
    def __init__(self, local_node_id, destination_key):
        super().__init__()
        self.type = "ClientLookUp"
        self.local_node_id = local_node_id
        self.destination_key = destination_key
    
    def __str__(self) -> str:
        return "ClientLookUp(localnode={}, key={})".format(self.local_node_id, self.local_node_id, self.destination_key)
    
# class Finish(Command):
#     def __init__(self):
#         super().__init__()
#         self.type = "Finish"
    
#     def __str__(self) -> str:
#         return "Finish()"

def parse_commands(commandfile):
    commands = []
    f2 = open(commandfile, 'r')
    commands_txt = f2.readlines()
    f2.close()
    for cmd in commands_txt:
        cmd_split = cmd.split(" ")
        if cmd_split[0] == "nodejoin":
            id = cmd_split[1].split("=")[-1][:-1]
            ip = cmd_split[2].split("=")[-1][:-1]
            port = cmd_split[3].split("=")[-1][:-1]
            commands.append(MakeNode(id,ip,port))
        if cmd_split[0] == "insert":
            key = cmd_split[1].split("=")[-1][:-1]
            val = cmd_split[2].split("=")[-1][:-1]
            print("|{}|{}|".format(key,val))
            commands.append(InsertKey(key,val))
        if cmd_split[0] == "look-up":
            localnode = cmd_split[1].split("=")[-1][:-1]
            key = cmd_split[2].split("=")[-1][:-1]
            commands.append(ClientLookUp(localnode,key))
    
    return commands


def execute(commands, dht):
    for command in commands:
        dht.process(commands)


if __name__ == '__main__':
    commandfile = 'command_small.txt'
    commands = parse_commands(commandfile)
    for cmd in commands:
        print(cmd)
