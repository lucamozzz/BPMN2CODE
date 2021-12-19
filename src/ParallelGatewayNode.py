from Node import Node


class ParallelGatewayNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id)
        self.type = 'ParallelGateway'
        self.exit = False
