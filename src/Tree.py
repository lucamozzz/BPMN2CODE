from Node import Node
from SequenceNode import SequenceNode


class Tree:

    def __init__(self):
        self.__root = None
        self.__size = 0
        self.__sons = list()
        self.__countOpen = 0
        self.__flagEndVisit = False
        self.__countChildSeq = 0

    def get_root(self):
        return self.__root

    def set_root(self, root=Node):
        self.__root = root

    def get_size(self):
        return self.__size

    def get_sons(self):
        return self.__sons

    def insert(self, node):
        if self.__root is None:
            self.set_root(node)
        else:
            self.__sons.append(node)
        self.__size += 1

    def insert_in(self, index, node):
        self.__sons.insert(index, node)

    def build_tree(self):
        self.__build_tree()
        self.__check_tree_is_correct()
        self.__case_loop()
        self.__visit_and_set_child_to_root()
        self.__setSequence()
        self.__complete_tree()
        return self

    def __build_tree(self):
        for node in self.__sons:
            if not node.isLeaf():
                for child in node.getChildren():
                    if child.getType() == 'IncomingNode':
                        id = child.getId()
                        flagIncoming = True
                        self.__set_child(child, id, node, flagIncoming)
                    elif child.getType() == 'OutgoingNode':
                        id = child.getId()
                        flagIncoming = False
                        self.__set_child(child, id, node, flagIncoming)

    def __set_child(self, child, id, node, flagIncoming):
        for n in self.__sons:
            for figlio in n.getChildren():
                if figlio.getType() == 'OutgoingNode' and flagIncoming:
                    if id == figlio.getId():
                        n.getChildren().remove(figlio)
                        node.getChildren().remove(child)
                        self.__addChildAndParentTo(node, n)
                elif figlio.getType() == 'IncomingNode' and not flagIncoming:
                    if id == figlio.getId():
                        self.__addChildAndParentTo(n, node)
                        n.getChildren().remove(figlio)
                        node.getChildren().remove(child)

    def __addChildAndParentTo(self, n, node):
        node.addChild(n)
        n.addParent(node)

    def __check_tree_is_correct(self):
        for nodo in self.__sons:
            for f in nodo.getChildren():
                if f.getType() == 'IncomingNode' or f.getType() == 'OutgoingNode':
                    self.__build_tree()

    def __case_loop(self):
        for n in self.__sons:
            if n.getType() == 'ExclusiveGateway':
                for p in n.getParents():
                    if p.getType() == 'ExclusiveGateway' and p.getLoop() and not n.getIsExit():
                        n.getParents().remove(p)
                        p.getChildren().remove(n)
                        n.setLoop(True)
                        n.setCondition(p.getCondition())
                        p.setCondition("")
                        p.setExit(True)
                        p.setLoop(True)

    def __set_child_to_root(self, n):
        if not n.getIsExit() and not n.getType() == 'EndEvent':
            for node in n.getParents():
                if node is not self.__sons[0]:
                    n.getParents().remove(node)
            if not self.__sons[0].getChildren().__contains__(n):
                n.addParent(self.__sons[0])
                self.__sons[0].addChild(n)
        return n

    def __visit_and_set_child_to_root(self):
        for n in self.__sons[0].getChildren():
            if n.getType() == 'ExclusiveGateway' or n.getType() == 'ParallelGateway':
                self.__check_if_new_child_of_root(n)
                self.__countOpen += 1
                self.__ric_component(n)
            else:
                self.__check_if_new_child_of_root(n)
                self.__ric_component(n)
            if self.check_if_sequence_of_root():
                break

    def check_if_sequence_of_root(self):
        if self.__countOpen == 0:
            self.__set_sequence_node_to_start()
            return True
        else:
            return False

    def __ric_component(self, figlio):
        self.__flagEndVisit = False
        for f in figlio.getChildren():
            if not self.__flagEndVisit:
                self.__check_if_new_child_of_root(f)
                if f.getType() == 'EndEvent':
                    self.__flagEndVisit = True
                    break
                if f.getType() != 'task':
                    if not f.getIsExit():
                        self.__countOpen += 1
                        self.__ric_component(f)
                    else:
                        self.__countOpen -= 1
                        self.__ric_component(f)
                else:
                    self.__ric_child_in_component(f)

    def __check_if_new_child_of_root(self, f):
        if self.__countOpen == 0:
            self.__set_child_to_root(f)

    def __ric_child_in_component(self, figlio):
        if not self.__flagEndVisit:
            self.__check_if_new_child_of_root(figlio)
            for child in figlio.getChildren():
                if child.getType() == 'task':
                    self.__check_if_new_child_of_root(child)
                    self.__ric_child_in_component(child)
                else:
                    if not child.getIsExit():
                        self.__ric_component(figlio)
                    else:
                        self.__countOpen -= 1
                        self.__ric_component(child)

    def __set_sequence_node_to_start(self):
        seq = SequenceNode(self.__sons[0].getId())
        seq.addParent(self.__sons[0])
        for child in self.__sons[0].getChildren():
            seq.addChild(child)
            child.getParents().remove(self.__sons[0])
            child.addParent(seq)
        for child in seq.getChildren():
            self.__sons[0].getChildren().remove(child)
        self.__sons[0].addChild(seq)
        self.insert(seq)

    def __setSequence(self):
        seq = None
        for figlio in self.__sons[0].getChildren():
            if figlio.getType() == "Sequence":
                for f in figlio.getChildren():
                    if f.getType() != 'task' and f.getType() != "Sequence":
                        self.__ric_set_sequence(f, seq)

    def __ric_set_sequence(self, nodoApertura, seq):
        for figlio in nodoApertura.getChildren():
            if figlio.getType() == "task":
                seq = self.__case_task_in_sequence(figlio, nodoApertura, seq)
            else:
                seq = self.__case_gateway_in_sequence(figlio, nodoApertura, seq)

    def __case_gateway_in_sequence(self, figlio, nodoApertura, seq):
        if not figlio.getIsExit() and figlio.getType() != 'EndEvent':
            if self.__countChildSeq >= 1:
                seq.addChild(figlio)
                self.__countChildSeq = 0
            else:
                seq = self.__setChildParent(figlio, nodoApertura)
            self.__ric_set_sequence(figlio, seq)
        else:
            for next in figlio.getChildren():
                if self.__sons[0].getChildren()[0].getChildren().__contains__(next):
                    self.__countChildSeq = 0
                    return
                else:
                    self.__ric_set_sequence(figlio, seq)
        return seq

    def __case_task_in_sequence(self, figlio, nodoApertura, seq):
        if self.__countChildSeq < 1:
            seq = self.__setChildParent(figlio, nodoApertura)
        else:
            seq.addChild(figlio)
        for nipote in figlio.getChildren():
            if not nipote.getIsExit():
                self.__countChildSeq += 1
                self.__ric_set_sequence(figlio, seq)
            else:
                exit = nipote
                self.__countChildSeq = 0
                if not exit.isLeaf():
                    for f in filter(lambda ff: not ff.getIsExit() and not ff.getType() == "EndEvent",
                                    exit.getChildren()):
                        for seq in filter(lambda s: s.getType() == "Sequence", self.__sons):
                            if seq.getChildren().__contains__(nodoApertura):
                                if not seq.getChildren().__contains__(f):
                                    self.__addChildAndParentTo(f, seq)
                                    self.__countChildSeq += 1
                                    if f.getType() != 'task':
                                        self.__countChildSeq = 0
                                    self.__ric_set_sequence(f, seq)
                                    break
            figlio.getChildren().remove(nipote)
        return seq

    def __setChildParent(self, figlio, nodoApertura):
        seq = SequenceNode(figlio.getId())
        seq.addParent(nodoApertura)
        nodoApertura.addChildIn(0, seq)
        nodoApertura.getChildren().remove(figlio)
        seq.addChild(figlio)
        for padre in figlio.getParents():
            figlio.getParents().remove(padre)
        figlio.addParent(seq)
        self.insert(seq)
        return seq

    to_remove = list()

    def __remove_parent_or_child_in_sequence_node(self):
        for seq in self.__sons:
            if seq.getType() == 'Sequence':
                for figlio in seq.getChildren():
                    for padre in figlio.getParents():
                        if padre.getType() != 'Sequence':
                            figlio.getParents().remove(padre)
                        if not figlio.getParents().__contains__(seq):
                            figlio.addParent(seq)
                    for child in figlio.getChildren():
                        if child.getType() != 'Sequence':
                            figlio.getChildren().remove(child)

    def __complete_tree(self):
        self.__remove_parent_or_child_in_sequence_node()
        for nodoExit in filter(lambda nEx: nEx.getIsExit(), self.__sons):
            self.to_remove.append(nodoExit)
            for node in self.__sons:
                if node.getChildren().__contains__(nodoExit):
                    node.getChildren().remove(nodoExit)
                if node.getParents().__contains__(nodoExit):
                    node.getParents().remove(nodoExit)
        for f in filter(lambda figlio: figlio.getType() == "EndEvent", nodoExit.getChildren()):
            nodoExit.getChildren().remove(f)
            self.to_remove.append(nodoExit)
        self.set_root(self.__sons[0])
        self.__sons.remove(self.__sons[0])
        self.__size -= 1
        self.__check_exitNode_and_remove()
        self.__remove_endEvent()
        self.__order_tree()

    def __check_exitNode_and_remove(self):
        for el in self.to_remove:
            for nodo in self.__sons:
                if el == nodo:
                    self.__sons.remove(nodo)
                    self.__size -= 1

    def __remove_endEvent(self):
        for n in self.__sons:
            if n.getType() == 'EndEvent':
                self.__sons.remove(n)
                self.__size -= 1
            if n.getIsExit():
                self.__sons.remove(n)
                self.__size -= 1

    def __order_tree(self):
        for gateway in self.__sons:
            if gateway.getType() == 'ExclusiveGateway':
                if len(gateway.getChildren()) > 1:
                    for figlio in gateway.getChildren():
                        if gateway.getChildren().index(figlio) == 1:
                            gateway.getChildren().remove(figlio)
                            gateway.addChildIn(0, figlio)