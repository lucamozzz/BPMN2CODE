from Node import Node


class StartNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'StartEvent', False)
