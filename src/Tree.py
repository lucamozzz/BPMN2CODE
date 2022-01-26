from Node import Node
from src.SequenceNode import SequenceNode


class Tree:

    def __init__(self):
        self.root = None
        self.size = 0
        self.depth = 0
        self.sons = list()
        self.countOpen = 0
        self.flagEnd = False
        self.flagExit = False
        self.temp_lis_to_exit_node = list()

    def get_root(self):
        return self.root

    def set_root(self, root=Node):
        self.root = root

    def get_size(self):
        return self.size

    def get_depth(self):
        return self.depth

    def get_sons(self):
        return self.sons

    def get_son_by_id(self, id):
        return self.get_sons().__getitem__(id)

    def insert(self, node):
        if self.root is None:
            self.set_root(node)
        else:
            self.sons.append(node)
        self.size += 1

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
            if p.getType() == 'ExclusiveGateway' and p.getLoop():
                n.getParents().remove(p)
                p.getChildren().remove(n)
                n.setLoop(True)
                p.setExit(True)
                p.setLoop(False)
                for figlio in p.getChildren():
                    if figlio.getType() != "EndEvent" and figlio != n:
                        for padreDiLoop in p.getParents():
                            padreDiLoop.addChild(figlio)
                            figlio.getParents().append(padreDiLoop)

    def __set_child_to_root(self, n):
        for figlio in n.getChildren():
            if not figlio.getIsExit() and not figlio.getType() == 'EndEvent':
                for node in figlio.getParents():
                    figlio.getParents().remove(node)
                if not self.sons[0].getChildren().__contains__(figlio):
                    figlio.addParent(self.sons[0])
                    self.sons[0].addChild(figlio)
            return figlio

    def __visit_and_set_child_to_root(self):
        for n in self.sons:
            if n.getType() == 'ExclusiveGateway' or n.getType() == 'ParallelGateway':
                if not n.getIsExit():
                    self.countOpen += 1
                    self.__visit(n)
                    if self.countOpen == 0:
                        self.__set_sequence_node_to_start()
                        break

    def __visit(self, n):
        for figlio in n.getChildren():
            if (figlio.getType() == 'ExclusiveGateway' and not figlio.getLoop()) or (
                    figlio.getType() == 'ParallelGateway'):
                if not figlio.getIsExit():
                    self.countOpen += 1
                else:
                    self.countOpen -= 1
                    self.__check_ric_on_new_child_of_root(figlio)
                self.ric_component(figlio)
            elif figlio.getType() == 'task':
                # se figlio è una foglia (task) e ha come figlio un nodo di uscita:
                self.ric_component(figlio)

    def ric_component(self, figlio):
        self.flagEnd = False
        node = None
        for f in figlio.getChildren():
            if f.getType() == 'EndEvent':
                self.flagEnd = True
                break
            if (f.getType() == 'ExclusiveGateway' and not f.getLoop()) or f.getType() != 'task':
                if not f.getIsExit():
                    self.countOpen += 1
                    self.ric_component(f)
                else:
                    self.__check_exit_node(f)
                    self.temp_lis_to_exit_node.append(f)
                    self.ric_component(f)
            else:
                if f.getType() == 'task':
                    for ff in f.getChildren():
                        if not ff.getIsExit():
                            self.ric_child_in_component(f)
                        else:
                            if self.flagExit is False and not self.temp_lis_to_exit_node.__contains__(ff):
                                self.flagExit = True
                                self.__check_exit_node(ff)
                                self.temp_lis_to_exit_node.append(ff)
                            elif self.flagExit:
                                self.flagExit = False
            node = f
        if not self.flagEnd:
            self.ric_component(node)

    def __check_exit_node(self, f):
        if not self.temp_lis_to_exit_node.__contains__(f):
            self.countOpen -= 1
            self.__check_ric_on_new_child_of_root(f)

    def __check_ric_on_new_child_of_root(self, f):
        if (self.countOpen == 0 and f.getType() != 'task') or \
                (self.countOpen == 0 and f.getType() == 'ExclusiveGateway' and not f.getLoop()):
            self.__set_child_to_root(f)

    def ric_child_in_component(self, figlio):
        # due casi: 1. il figlio è un altra foglia, 2. il figlio è un component
        if figlio.getType() == 'task':
            for child in figlio.getChildren():
                if child.getType() == 'task':
                    self.ric_child_in_component(child)
                else:
                    if not child.getIsExit() and child.getType() == 'ParallelGateway' or \
                            (child.getType() == 'ExclusiveGateway' and not child.getLoop() and not child.getIsExit()):
                        self.countOpen += 1
                        self.ric_component(child)
                    elif child.getType() == 'ExclusiveGateway' and child.getLoop():
                        self.ric_component(child)
                    else:
                        self.countOpen -= 1
                        self.__check_ric_on_new_child_of_root(child)
        else:
            self.ric_component(figlio)

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
                for child in figlio.getChildren():
                    if child.getType() != "task":
                        self.__ric_set_sequence(child, seq)

    count = 0

    def __ric_set_sequence(self, nodoApertura, seq):
        for figlio in nodoApertura.getChildren():
            if figlio.getType() == "task":
                if self.count < 1:
                    seq = self.setChildParent(figlio, nodoApertura)
                else:
                    seq.addChild(figlio)
                    if figlio.getType() != "task":
                        self.__ric_set_sequence(figlio, seq)
                for nipote in figlio.getChildren():
                    if not nipote.getIsExit():
                        self.count += 1
                        self.__ric_set_sequence(figlio, seq)
                    else:
                        exit = nipote
                        self.count = 0
                        if not exit.isLeaf():
                            for f in exit.getChildren():
                                if not f.getIsExit():
                                    for seq in self.sons:
                                        if seq.getType() == "Sequence":
                                            if seq.getId() == nodoApertura.getId():
                                                if not seq.getChildren().__contains__(f):
                                                    seq.addChild(f)
                                                    self.__ric_set_sequence(f, seq)
            else:
                if self.count >= 1:
                    seq.addChild(figlio)
                    self.count = 0
                else:
                    seq = self.setChildParent(figlio, nodoApertura)
                self.__ric_set_sequence(figlio, seq)

    def setChildParent(self, figlio, nodoApertura):
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
    def __complete_tree(self):
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
        self.__remove_end_event()

    def __check_exitNode_and_remove(self):
        for el in self.to_remove:
            for nodo in self.sons:
                if el == nodo:
                    self.sons.remove(nodo)
                    self.size -= 1

    def __remove_end_event(self):
        for n in self.sons:
            if n.getType() == 'EndEvent':
                self.sons.remove(n)
                self.size -= 1
            if n.getIsExit():
                self.sons.remove(n)
                self.size -= 1