from Node import Node


class EndNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'EndEvent', False)
