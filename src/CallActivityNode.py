from Node import Node


class CallActivityNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id)
        self.type = 'CallActivity'
        self.name = ''
