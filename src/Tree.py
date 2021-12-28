from Node import Node
from src.ExclusiveGatewayNode import ExclusiveGatewayNode
from src.IncomingNode import IncomingNode
from src.OutgoingNode import OutgoingNode


class Tree:

    def __init__(self):
        self.root = None
        self.size = 0
        self.depth = 0
        self.sons = list()

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

    def insert(self, node=Node):
        if self.root is None:
            self.set_root(node)
        else:
            self.sons.append(node)
        self.size += 1

    def visit_pre_order(self, root):
        nodi_figli = list()
        nodi_nipoti = list()
        for node in root.getChildren():
            nodi_figli.append(node)  # tutti i figli della root.
        print(nodi_figli)
        for child_node in nodi_figli:
            print(child_node.getChildren())
            for n in child_node.getChildren():  # tutti i figli di nodi_figli
                nodi_nipoti.append(n)
                while not n.isLeaf():  # fino a che il child_node non è una foglia, cerca i nodi figli e inseriscili
                    for figlio in n.getChildren():
                        nodi_nipoti.append(figlio)
                    n = figlio
        print(nodi_figli)
        print(nodi_nipoti)

    def build_tree(self):
        # todo - gestire il caso in cui un nodo è loop.
        #
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
        self.complete_tree()

    def __set_child_to_root(self):
        for n in self.sons:
            if n.getIsExit():
                for figlio in n.getChildren():
                    if not figlio.getIsExit() and not figlio.getType() == 'EndEvent':
                        for node in figlio.getParents():
                            figlio.getParents().remove(node)
                        figlio.addParent(self.sons[0])
                        self.sons[0].addChild(figlio)

    def complete_tree(self):
        for n in self.sons:
            if n.getIsExit():
                self.__set_child_to_root()
                for node in self.sons:
                    if node.getChildren().__contains__(n):
                        node.getChildren().remove(n)
                self.sons.remove(n)
            #     verificare, not ok
            if n.getType() == 'EndEvent':
                self.sons.remove(n)

