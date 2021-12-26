from Node import Node


class AssociationNode(Node):

    def __init__(self, node_id):
        super().__init__(node_id, 'Association', False)
