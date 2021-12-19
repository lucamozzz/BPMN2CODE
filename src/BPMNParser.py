import xml.etree.ElementTree as et
from AnnotationNode import AnnotationNode
from CallActivityNode import CallActivityNode
from EndNode import EndNode
from ExclusiveGatewayNode import ExclusiveGatewayNode
from ParallelGatewayNode import ParallelGatewayNode
from StartNode import StartNode


class BPMNParser:

    def __init__(self, source):
        self.source = source
        self.root = et.parse(source).getroot().find('{http://www.omg.org/spec/BPMN/20100524/MODEL}process')
        self.connections = []
        self.annotations = []
        self.nodes = []

    def parse_nodes(self):
        for child in self.root:
            if child.tag.__contains__('sequenceFlow'):
                self.connections.append(child)
            if child.tag.__contains__('association'):
                self.connections.append(child)
            elif child.tag.__contains__('startEvent'):
                node = StartNode(child.get('id'))
                self. nodes.append(node)
            elif child.tag.__contains__('endEvent'):
                node = EndNode(child.get('id'))
                self.nodes.append(node)
            elif child.tag.__contains__('exclusiveGateway'):
                node = ExclusiveGatewayNode(child.get('id'))
                self.nodes.append(node)
            elif child.tag.__contains__('parallelGateway'):
                node = ParallelGatewayNode(child.get('id'))
                self.nodes.append(node)
            elif child.tag.__contains__('task'):
                node = CallActivityNode(child.get('id'))
                self.nodes.append(node)
            elif child.tag.__contains__('textAnnotation'):
                id = child.get('id')
                text = child[0].text
                annotation = AnnotationNode(id, text)
                self.annotations.append(annotation)

    def connect_nodes(self):
        for connection in self.connections:
            if connection.tag.__contains__('association'):
                for el in self.nodes:
                    if el.id == connection.get('sourceRef'):
                        node = el
                for annotation in self.annotations:
                    if annotation.id == connection.get('targetRef'):
                        if annotation.value == 'exit':
                            node.setExit(True)
                        elif annotation.value == 'loop':
                            node.setLoop(True)
            else:
                for el in self.nodes:
                    if el.id == connection.get('sourceRef'):
                        parent = el
                    elif el.id == connection.get('targetRef'):
                        child = el
                parent.addChild(child.id)
                child.addParent(parent.id)

    def getConnections(self):
        return self.connections

    def getNodes(self):
        return self.nodes

    def getAnnotations(self):
        return self.annotations