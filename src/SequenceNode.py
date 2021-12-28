from Node import Node


class SequenceNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'Sequence', False)
