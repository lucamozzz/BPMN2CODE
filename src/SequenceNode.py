from Node import Node


class ExclusiveGatewayNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'Sequence', False)
