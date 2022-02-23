from Node import Node


class IncomingNode(Node):
    def __init__(self, node_id):
        super().__init__(node_id, 'IncomingNode', False)

