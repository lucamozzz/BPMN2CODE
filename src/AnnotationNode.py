from Node import Node


class AnnotationNode(Node):

    def __init__(self, node_id, value):
        super().__init__(node_id, 'Annotation', False)
        self.__value = value

    def getValue(self):
        return self.__value
