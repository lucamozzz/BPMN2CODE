from Node import Node


class AnnotationNode(Node):

    def __init__(self, node_id, value):
        super().__init__(node_id)
        self.type = 'Annotation'
        self.value = value
