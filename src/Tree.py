from Node import Node
from SequenceNode import SequenceNode


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
                    self.ric_component(n)
            elif n.getType() == 'task':
                self.__check_if_new_child_of_root(n)
                self.ric_component(n)
                if self.countOpen == 0:
                    self.__set_sequence_node_to_start()
                    break
            else:
                continue
            if self.countOpen == 0:
                self.__set_sequence_node_to_start()
                break

    def ric_component(self, figlio):
        self.flagEnd = False
        for f in figlio.getChildren():
            if not self.flagEnd:
                self.__check_if_new_child_of_root(f)
                if f.getType() == 'EndEvent':
                    self.flagEnd = True
                    break
                if f.getType() != 'task':
                    if not f.getIsExit():
                        self.countOpen += 1
                        self.ric_component(f)
                    else:
                        self.countOpen -= 1
                        self.ric_component(f)
                elif f.getType() == 'task':
                    self.ric_child_in_component(f)

    def __check_exit_node(self, f):
        if not self.temp_lis_to_exit_node.__contains__(f):
            self.countOpen -= 1
            self.__check_if_new_child_of_root(f)

    def __check_if_new_child_of_root(self, f):
        if self.countOpen == 0:
            self.__set_child_to_root(f)

    def ric_child_in_component(self, figlio):
        if not self.flagEnd:
            self.__check_if_new_child_of_root(figlio)
            for child in figlio.getChildren():
                if child.getType() == 'task':
                    self.__check_if_new_child_of_root(child)
                    self.ric_child_in_component(child)
                else:
                    if child.getType() != 'task':
                        if not child.getIsExit():
                            self.ric_component(figlio)
                        else:
                            self.countOpen -= 1
                            self.ric_component(child)

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
                self.__ric_set_sequence(figlio, seq)

    count = 0

    def __ric_set_sequence(self, nodoApertura, seq):
        for figlio in nodoApertura.getChildren():
            if not figlio.isVisited():
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
                                    if not f.getIsExit() and not f.isVisited():
                                        for seq in self.sons:
                                            if seq.getType() == "Sequence":
                                                if seq.getId() == nodoApertura.getId():
                                                    if not seq.getChildren().__contains__(f):
                                                        f.setVisited(True)
                                                        seq.addChild(f)
                                                        f.addParent(seq)
                                                        self.count += 1
                                                        self.__ric_set_sequence(f, seq)
                                                        break
                                                        # for n in f.getChildren():
                                                        #     if n.getType() is not "Sequence":
                                                        #         f.getChildren().remove(n)
                                                        # for p in f.getParents():
                                                        #     if p.getType() is not "Sequence":
                                                        #         f.getParents().remove(p)
                        figlio.getChildren().remove(nipote)
                else:
                    if self.count >= 1:
                        # if not figlio.getIsExit():
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
