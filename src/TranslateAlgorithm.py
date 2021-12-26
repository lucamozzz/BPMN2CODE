import xml.etree.ElementTree as et

import switcher as switcher

from AnnotationNode import AnnotationNode
from CallActivityNode import CallActivityNode
from EndNode import EndNode
from ExclusiveGatewayNode import ExclusiveGatewayNode
from ParallelGatewayNode import ParallelGatewayNode
from StartNode import StartNode


def synchronized(self, children):
    return children


class TranslateAlgorithm:

    def translate(self, node):
        if node.getIsExit():
            return
        else:
            children = node.getChildren()
            switcher = {
                node.getType() == 'ExclusiveGateway' and node.loop == False:
                    "If node.condition :" \
                    "    " + self.translate(children[0]) + \
                    "else :" \
                    "    " + self.translate(children[1]),
                node.getType() == 'ExclusiveGateway' and node.loop == True:
                    "while(True):" \
                    "    " + self.translate(children[0]) + \
                    "if node.condition:" \
                    "    break",
                node.getType() == 'ParallelGateway':
                    "for x in synchronized(children): \
                                self.translate(x)",
                node.getType() == 'Sequence':
                    "for x in children:  \
                                self.translate(x)",
                node.getType() == 'CallActivity':
                    " " + self.translate(node.name)
            }
        return switcher
