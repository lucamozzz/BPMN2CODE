from Node import Node


class CallActivityNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'task', False)
        self.name = ''

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name
