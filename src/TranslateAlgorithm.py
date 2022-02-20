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
            output = self.outputIniziale()
            for x in children:
                output += self.translate(x)
        if node.getType() == 'ExclusiveGateway' and node.loop == False:
            output = self.indentationMethod(node) + "if " + node.condition + ":" + " \n" + self.translate(
                children[0]) + self.indentationMethod(node) + "else: \n " + self.translate(
                children[1]) + "\n"
        elif node.getType() == 'ExclusiveGateway' and node.loop == True:
            output = self.indentationMethod(node) + "while " + node.condition + ": \n " + self.translate(
                children[0]) + "\n"
        elif node.getType() == 'ParallelGateway':
            output += self.indentationMethod(node) + "runInParallel("
            nChildren = self.nChildren(node)
            i = 0
            while i < nChildren:
                output += self.translate(children[i])
                if nChildren - i != 1:
                    output += ", "
                i += i + 1
            output += ")\n"

        elif node.getType() == 'Sequence':
            for x in children:
                output += self.translate(x)
        elif node.getType() == 'task':
            parents = node.getParents()
            grandParent = parents[0].getParents()
            accapo = ""
            if grandParent[0].getType() != 'ParallelGateway':
                accapo += "\n"
            output = self.indentationMethod(node) + node.name + accapo
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
            i += "\t\t"
        elif node.getType() == 'Sequence' and parents[0].getType() == 'ParallelGateway':
            return ""
        elif parents[0].getType() == 'Sequence' or parents[0].getType() == 'ParallelGateway':
            i += self.indentationMethod(parents[0])
        else:
            i += "\t" + self.indentationMethod(parents[0])
        return i

    def nChildren(self, node):
        i = 0
        for x in node.getChildren():
            i += 1
        return i

    def outputIniziale(self):
        output = "from multiprocessing import Process\n\n"
        output += "class Result:\n\n"
        output += "\tdef runInParallel(*fns):\n\t\tproc = []\n\t\tfor fn in fns:\n\t\t\tp = Process(" \
                  "target=fn)\n\t\t\tp.start()\n\t\t\tproc.append(p)\n\t\tfor p in " \
                  "proc:\n\t\t\tp.join()\n\n\n"
        output += "if __name__ == '__main__':\n"
        return output
