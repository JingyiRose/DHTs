from env_dist import *
import random



class Client:

    def __init__(self, local_node, k, lookup_id, write_to = "reply.txt"):
        self.local_node = local_node
        self.query = k
        self.lookup_id = lookup_id
        self.req_complete = False
        self.in_queue = []
        self.client_id = random.choice(range(10000,99999))
        # self.write_to = write_to[:-4] + str(self.client_id) + write_to[-4:]
        self.write_to = write_to

    
    def make_query(self):
        req = ClientRequest(self, self.local_node, self.query, content = "Look up {}".format(self.query), proximity = "local", id = self.lookup_id)
        req.send()
        # while True:
        #     if len(self.in_queue) == 0:
        #         time.sleep(1)
        #     else:
        #         rep = self.in_queue.pop(0)
        #         self.process(rep)

    def wake(self):
        rep = self.in_queue.pop(0)
        self.req_complete = True
        # print("Query {} key = {} = value {}".format(self.lookup_id, self.query, rep.content[-10:]))
        f = open(self.write_to, 'a')
        f.write("Query {} key = {} = value {}\n".format(self.lookup_id, self.query, rep.content[-10:]))
        f.close()



    # def process(self, rep):
    #     # process reply
    #     self.req_complete = True
    #     # print("GOT REPLY! {}".format(reply))

