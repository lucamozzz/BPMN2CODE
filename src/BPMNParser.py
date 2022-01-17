import xml.etree.ElementTree as et
from AnnotationNode import AnnotationNode
from CallActivityNode import CallActivityNode
from EndNode import EndNode
from ExclusiveGatewayNode import ExclusiveGatewayNode
from ParallelGatewayNode import ParallelGatewayNode
from StartNode import StartNode
from Tree import Tree
from src.IncomingNode import IncomingNode
from src.OutgoingNode import OutgoingNode


class BPMNParser:

    def __init__(self, source):
        self.tree = Tree()
        self.source = source
        self.root = et.parse(source).getroot().find('{http://www.omg.org/spec/BPMN/20100524/MODEL}process')
        self.tree.set_root(self.root)
        self.connections = []
        self.annotations = []
        self.nodes = []
        self.sequenceFlows = []

    def parse_nodes(self):
        for child in self.root:
            # --NODI PER SETTARE NODO EXIT O LOOP
            if child.tag.__contains__('association'):
                self.connections.append(child)
            elif child.tag.__contains__('textAnnotation'):
                id = child.get('id')
                text = child[0].text
                annotation = AnnotationNode(id, text)
                self.annotations.append(annotation)

    def object_type_of_node(self, child):
        node = ''
        if child.tag.__contains__('startEvent'):
            node = StartNode(child.get('id'))
        elif child.tag.__contains__('endEvent'):
            node = EndNode(child.get('id'))
        elif child.tag.__contains__('exclusiveGateway'):
            node = ExclusiveGatewayNode(child.get('id'))
            self.__set_attrib_to_node(child, node)
        elif child.tag.__contains__('parallelGateway'):
            node = ParallelGatewayNode(child.get('id'))
        elif child.tag.__contains__('task'):
            node = CallActivityNode(child.get('id'))
            self.__set_attrib_to_node(child, node)
        return node

    def __set_attrib_to_node(self, child, node):
        for key in child.attrib:
            if key == 'name':
                if node.getType() == 'task':
                    node.setName(child.attrib[key])
                elif node.getType() == 'ExclusiveGateway':
                    node.setCondition(child.attrib[key])

    def connect_nodes(self):
        self.__set_child_incoming_outgoing()
        self.__set_exit_or_loop_node()
        for n in self.nodes:
            self.tree.insert(n)

    def getConnections(self):
        return self.connections

    def getNodes(self):
        return self.nodes

    def getAnnotations(self):
        return self.annotations

    def getSequenceFlows(self):
        return self.sequenceFlows

    def __set_child_incoming_outgoing(self):
        for child in self.root:
            tag_type = child.tag[45:len(child.tag)]
            if tag_type == 'association' or tag_type == 'textAnnotation':
                continue
            elif tag_type == 'sequenceFlow':
                self.sequenceFlows.append(child)
            else:
                node = self.object_type_of_node(child)
                for conn in child:
                    node.addChild(self.__create_node_in_out(conn))
                    if not self.nodes.__contains__(node):
                        self.nodes.append(node)

    def __set_exit_or_loop_node(self):
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

    def __create_node_in_out(self, conn):
        node = ''
        if conn.tag.__contains__('incoming'):
            node = IncomingNode(conn.text)
        elif conn.tag.__contains__('outgoing'):
            node = OutgoingNode(conn.text)
        return node
