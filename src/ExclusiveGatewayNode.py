from Node import Node


class ExclusiveGatewayNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'ExclusiveGateway', False)
        self.condition = ''
        self.loop = False

    def setExit(self, exit):
        self.isExit = exit

    def setLoop(self, loop):
        self.loop = loop

    def setCondition(self, condition):
        self.condition = condition

    def getCondition(self):
        return self.condition

    def getLoop(self):
        return self.loop
