

class Contact:

    def __init__(self, ip_address, port, node_id):

        self.ip_address = ip_address
        self.port = port
        self.node_id = node_id

    def __str__(self) -> str:
        return "<Contact: ip = {}, port = {}, node_id = {}>".format(self.ip_address, self.port, self.node_id)


