import xml.etree.ElementTree as et
from multiprocessing import Process

import switcher as switcher

from AnnotationNode import AnnotationNode
from CallActivityNode import CallActivityNode
from EndNode import EndNode
from ExclusiveGatewayNode import ExclusiveGatewayNode
from ParallelGatewayNode import ParallelGatewayNode
from StartNode import StartNode


class TranslateAlgorithm:

    def translate(self, node):
        children = node.getChildren()
        output = ""
        if node.getType() == 'StartEvent':
            for x in children:
                output += self.translate(x)
        if node.getType() == 'ExclusiveGateway' and node.loop == False:
            output = self.nParents(node) + "if " + node.condition + ":" + " \n" + self.nParents(
                children[0]) + self.translate(
                children[0]) + "\n" + self.nParents(node) + "else : \n " + self.nParents(children[1]) + self.translate(
                children[1]) + "\n"
        elif node.getType() == 'ExclusiveGateway' and node.loop == True:
            output = self.nParents(node) + "while(True): \n " + self.nParents(children[0]) + self.translate(
                children[0]) + "\n" + self.nParents(children[0]) + "if " + node.condition + ":" + "\n " + self.nParents(
                children[0]) + "break\n"
        elif node.getType() == 'ParallelGateway':
            output = self.nParents(node) + "runInParallel(children) :\n"
            output += self.runInParallel(children, output)
        elif node.getType() == 'Sequence':
            output = self.nParents(node) + "for x in children: \n"
            for x in children:
                output += self.translate(x) + "\n"
        elif node.getType() == 'task':
            output = self.nParents(node) + node.name + "\n"
        return output

    def runInParallel(self, children, output):
        proc = []
        for x in children:
            p = Process(name=self.translate(x))
            p.start()
            output += self.nParents(x) + str(p.name)
            proc.append(p)
        for p in proc:
            p.join()
        return output

    def nParents(self, node):
        i = ""
        for x in node.getParents():
            i += "\t"
        return i
