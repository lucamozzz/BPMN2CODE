
class Node:

    def __init__(self, node_id):
        self.id = node_id
        self.parents = []
        self.children = []

    def getId(self):
        return self.id

    def getParents(self):
        return self.parents

    def getChildren(self):
        return self.children

    def addParent(self, parent):
        self.parents.append(parent)

    def addChild(self, child):
        self.children.append(child)
