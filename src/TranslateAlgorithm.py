import xml.etree.ElementTree as et
from multiprocessing import Process

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
            output = self.indentationMethod(node) + "if " + node.condition + ":" + " \n" + self.translate(
                children[0]) + self.indentationMethod(node) + "else : \n " + self.translate(
                children[1]) + "\n"
        elif node.getType() == 'ExclusiveGateway' and node.loop == True:
            output = self.indentationMethod(node) + "while(True): \n " + self.translate(
                children[0]) + self.indentationMethod(
                children[0]) + "if " + node.condition + ":" + "\n " + self.indentationMethod(
                children[0]) + "\tbreak\n"
        elif node.getType() == 'ParallelGateway':
            output = self.indentationMethod(node) + "runInParallel(children) :\n"
            output += self.runInParallel(children, output)
        elif node.getType() == 'Sequence':
            stringForChildren = ""
            if self.nChildren(node) != 1:
                stringForChildren = "for x in children: "
            output = self.indentationMethod(node) + stringForChildren + "\n"
            for x in children:
                output += self.translate(x)
        elif node.getType() == 'task':
            output = self.indentationMethod(node) + node.name + "\n"
        return output

    def runInParallel(self, children, output):
        proc = []
        for x in children:
            p = Process(name=self.translate(x))
            p.start()
            output += self.indentationMethod(x) + str(p.name)
            proc.append(p)
        for p in proc:
            p.join()
        return output

    def indentationMethod(self, node):
        i = ""
        parents = node.getParents()
        if parents[0].getType() == 'StartEvent':
            i += ""
        elif parents[0].getType() == 'Sequence' and self.nChildren(parents[0]) == 1:
            i += self.indentationMethod(parents[0])
        else:
            i += "\t" + self.indentationMethod(parents[0])
        return i

    def nChildren(self, node):
        i = 0
        for x in node.getChildren():
            i += 1
        return i
