from Node import Node


class ExclusiveGatewayNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id)
        self.type = 'ExclusiveGateway'
        self.condition = ''
        self.exit = False
        self.loop = False

    def setExit(self, exit):
        self.exit = exit

    def setLoop(self, loop):
        self.loop = loop