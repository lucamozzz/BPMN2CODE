from Node import Node


class ExclusiveGatewayNode(Node):

    def __init__(self, node_id, isExit):
        super().__init__(node_id, 'ExclusiveGateway', isExit)
        self.condition = ''
        self.loop = False

    def setLoop(self, loop):
        self.loop = loop