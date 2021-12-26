from Node import Node


class AnnotationNode(Node):

    def __init__(self, node_id, value):
        super().__init__(node_id, 'Annotation')
        self.value = value
