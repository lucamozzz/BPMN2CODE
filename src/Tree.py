from Node import Node
from SequenceNode import SequenceNode


class Tree:

    def __init__(self):
        self.root = None
        self.size = 0
        self.sons = list()
        self.countOpen = 0
        self.flagEndVisit = False
        self.flagExitSequenceNode = False

    def get_root(self):
        return self.root

    def set_root(self, root=Node):
        self.root = root

    def get_size(self):
        return self.size

    def get_sons(self):
        return self.sons

    def insert(self, node):
        if self.root is None:
            self.set_root(node)
        else:
            self.sons.append(node)
        self.size += 1

    def insert_in(self, index, node):
        self.sons.insert(index, node)

    def build_tree(self):
        self.__build_tree()
        self.__check_tree()
        self.__case_loop()
        self.__visit_and_set_child_to_root()
        self.__setSequence()
        self.__complete_tree()
        return self

    def __build_tree(self):
        for node in self.sons:
            if not node.isLeaf():
                for child in node.getChildren():
                    if child.type == 'IncomingNode':
                        id = child.id
                        for n in self.sons:
                            for figlio in n.getChildren():
                                if figlio.type == 'OutgoingNode':
                                    if id == figlio.id:
                                        n.getChildren().remove(figlio)
                                        node.getChildren().remove(child)
                                        node.addParent(n)
                                        n.addChild(node)
                    elif child.type == 'OutgoingNode':
                        id = child.id
                        for n in self.sons:
                            for figlio in n.getChildren():
                                if figlio.type == 'IncomingNode':
                                    if id == figlio.id:
                                        node.addChild(n)
                                        n.addParent(node)
                                        n.getChildren().remove(figlio)
                                        node.getChildren().remove(child)

    def __check_tree(self):
        for nodo in self.sons:
            for f in nodo.getChildren():
                if f.getType() == 'IncomingNode' or f.getType() == 'OutgoingNode':
                    self.__build_tree()

    def __case_loop(self):
        for n in self.sons:
            if n.getType() == 'ExclusiveGateway':
                self.__node_loop(n)

    def __node_loop(self, n):
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
                if node is not self.sons[0]:
                    n.getParents().remove(node)
            if not self.sons[0].getChildren().__contains__(n):
                n.addParent(self.sons[0])
                self.sons[0].addChild(n)
        return n

    def __visit_and_set_child_to_root(self):
        for n in self.sons[0].getChildren():
            if n.getType() == 'ExclusiveGateway' or n.getType() == 'ParallelGateway':
                if not n.getIsExit():
                    self.__check_if_new_child_of_root(n)
                    self.countOpen += 1
                    self.__ric_component(n)
            elif n.getType() == 'task':
                self.__check_if_new_child_of_root(n)
                self.__ric_component(n)
                if self.countOpen == 0:
                    self.__set_sequence_node_to_start()
                    break
            else:
                continue
            if self.countOpen == 0:
                self.__set_sequence_node_to_start()
                break

    def __ric_component(self, figlio):
        self.flagEndVisit = False
        for f in figlio.getChildren():
            if not self.flagEndVisit:
                self.__check_if_new_child_of_root(f)
                if f.getType() == 'EndEvent':
                    self.flagEndVisit = True
                    break
                if f.getType() != 'task':
                    if not f.getIsExit():
                        self.countOpen += 1
                        self.__ric_component(f)
                    else:
                        self.countOpen -= 1
                        self.__ric_component(f)
                elif f.getType() == 'task':
                    self.__ric_child_in_component(f)

    def __check_if_new_child_of_root(self, f):
        if self.countOpen == 0:
            self.__set_child_to_root(f)

    def __ric_child_in_component(self, figlio):
        if not self.flagEndVisit:
            self.__check_if_new_child_of_root(figlio)
            for child in figlio.getChildren():
                if child.getType() == 'task':
                    self.__check_if_new_child_of_root(child)
                    self.__ric_child_in_component(child)
                else:
                    if child.getType() != 'task':
                        if not child.getIsExit():
                            self.__ric_component(figlio)
                        else:
                            self.countOpen -= 1
                            self.__ric_component(child)

    def __set_sequence_node_to_start(self):
        seq = SequenceNode(self.sons[0].getId())
        seq.addParent(self.sons[0])
        for child in self.sons[0].getChildren():
            seq.addChild(child)
            child.getParents().remove(self.sons[0])
            child.addParent(seq)
        for child in seq.getChildren():
            self.sons[0].getChildren().remove(child)
        self.sons[0].addChild(seq)
        self.insert(seq)

    def __setSequence(self):
        seq = None
        for figlio in self.sons[0].getChildren():
            if figlio.getType() == "Sequence":
                for f in figlio.getChildren():
                    if f.getType() != 'task' and f.getType() != "Sequence":
                        self.flagExitSequenceNode = False
                        self.__ric_set_sequence(f, seq)

    countChildSeq = 0
    flagExitSequenceNode = False

    def __ric_set_sequence(self, nodoApertura, seq):
        # todo - refactoring. [fixare] bug.
        for figlio in nodoApertura.getChildren():
            if not self.flagExitSequenceNode:
                if figlio.getType() == "task":
                    if not self.sons[0].getChildren()[0].getChildren().__contains__(figlio):
                        if self.countChildSeq < 1:
                            seq = self.__setChildParent(figlio, nodoApertura)
                        else:
                            seq.addChild(figlio)
                        for nipote in figlio.getChildren():
                            if not nipote.getIsExit():
                                self.countChildSeq += 1
                                self.__ric_set_sequence(figlio, seq)
                            else:
                                exit = nipote
                                self.countChildSeq = 0
                                if not exit.isLeaf():
                                    for f in exit.getChildren():
                                        if not f.getIsExit() and not f.getType() == 'EndEvent':
                                            for seq in self.sons:
                                                if seq.getType() == "Sequence":
                                                    if seq.getId() == nodoApertura.getId():
                                                        if not seq.getChildren().__contains__(f):
                                                            seq.addChild(f)
                                                            f.addParent(seq)
                                                            self.countChildSeq += 1
                                                            if f.getType() != 'task':
                                                                self.countChildSeq = 0
                                                            self.__ric_set_sequence(f, seq)
                                                            break
                            figlio.getChildren().remove(nipote)
                    else:
                        self.flagExitSequenceNode = True
                        self.countChildSeq = 0
                        break
                else:
                    if not self.sons[0].getChildren()[0].getChildren().__contains__(figlio):
                        if not figlio.getIsExit() and figlio.getType() != 'EndEvent':
                            if self.countChildSeq >= 1:
                                seq.addChild(figlio)
                                self.countChildSeq = 0
                            else:
                                seq = self.__setChildParent(figlio, nodoApertura)
                            self.__ric_set_sequence(figlio, seq)
                        else:
                            for next in figlio.getChildren():
                                if self.sons[0].getChildren()[0].getChildren().__contains__(next):
                                    self.countChildSeq = 0
                                    return
                                else:
                                    self.__ric_set_sequence(figlio, seq)
                    else:
                        self.flagExitSequenceNode = True
                        self.countChildSeq = 0
                        break

    def __setChildParent(self, figlio, nodoApertura):
        seq = SequenceNode(figlio.id)
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
        for seq in self.sons:
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
        for n in self.sons:
            if n.getIsExit():
                self.to_remove.append(n)
                for node in self.sons:
                    if node.getChildren().__contains__(n):
                        node.getChildren().remove(n)
                    if node.getParents().__contains__(n):
                        node.getParents().remove(n)
            for f in n.getChildren():
                if f.getType() == 'EndEvent':
                    n.getChildren().remove(f)
                    self.to_remove.append(n)
        self.set_root(self.sons[0])
        self.sons.remove(self.sons[0])
        self.size -= 1
        self.__check_exitNode_and_remove()
        self.__remove_endEvent()
        self.order_tree()

    def __check_exitNode_and_remove(self):
        for el in self.to_remove:
            for nodo in self.sons:
                if el == nodo:
                    self.sons.remove(nodo)
                    self.size -= 1

    def __remove_endEvent(self):
        for n in self.sons:
            if n.getType() == 'EndEvent':
                self.sons.remove(n)
                self.size -= 1
            if n.getIsExit():
                self.sons.remove(n)
                self.size -= 1

    old_tree = None

    def order_tree(self):
        for gateway in self.sons:
            if gateway.getType() == 'ExclusiveGateway':
                if len(gateway.getChildren()) > 1:
                    for figlio in gateway.getChildren():
                        if gateway.getChildren().index(figlio) == 1:
                            gateway.getChildren().remove(figlio)
                            gateway.addChildIn(0, figlio)
