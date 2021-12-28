from Node import Node


class ParallelGatewayNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'ParallelGateway', False)

    def setExit(self, exit):
        self.isExit = exit
