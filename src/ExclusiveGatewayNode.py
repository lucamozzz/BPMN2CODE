from Node import Node


class ExclusiveGatewayNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'ExclusiveGateway', False)
        self.__condition = ''
        self.__loop = False

    def setExit(self, exit):
        self.isExit = exit

    def setLoop(self, loop):
        self.__loop = loop

    def setCondition(self, condition):
        self.__condition = condition

    def getCondition(self):
        return self.__condition

    def getLoop(self):
        return self.__loop
