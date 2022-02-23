from Node import Node


class OutgoingNode(Node):
    def __init__(self, node_id):
        super().__init__(node_id, 'OutgoingNode', False)
