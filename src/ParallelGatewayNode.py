from Node import Node


class ParallelGatewayNode(Node):

    def __init__(self, node_id, isExit):
        super().__init__(node_id, 'ParallelGateway', isExit)
