from Node import Node


class CallActivityNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'task', False)
        self.__name = ''

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name
