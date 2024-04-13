from env import *
import os

class Command:
    # use for controller
    def __init__(self):
        self.type = None
    
class MakeKey(Command):
    def __init__(self, key, val):
        super().__init__()
        self.key = key
        self.val = val
        self.type = "MakeKey"
    
    def __str__(self) -> str:
        return "MakeKey({},{})".format(self.key, self.val)
    
class MakeNode(Command):
    def __init__(self, key, val):
        super().__init__()
        self.key = key
        self.val = val
        self.type = "MakeNode"
    
    def __str__(self) -> str:
        return "MakeNode({})".format(self.key)

class ClientLookUp(Command):
    def __init__(self, lookup_id, local_node_id, dest_key):
        super().__init__()
        self.type = "ClientLookUp"
        self.lookup_id = lookup_id
        self.local_node_id = local_node_id
        self.dest_key = dest_key
    
    def __str__(self) -> str:
        return "ClientLookUp({},{},{})".format(self.lookup_id, self.local_node_id, self.dest_key)
    
class Finish(Command):
    def __init__(self):
        super().__init__()
        self.type = "Finish"
    
    def __str__(self) -> str:
        return "Finish()"

def parse(testfile, keyvalfile):
    commands = []
    f2 = open(testfile, 'r')
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


def execute(commands, dht):
    for command in commands:
        dht.process(commands)


if __name__ == '__main__':
    testfile = 'log.txt'
    keyvalfile = 'keyval.txt'
    commands = parse(testfile, keyvalfile)
    for command in commands:
        print(command)
