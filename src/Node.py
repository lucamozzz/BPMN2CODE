class Node:

    def __init__(self, node_id, type, isExit):
        self.id = node_id
        self.parents = list()
        self.children = list()
        self.type = type
        self.isExit = isExit

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

    def isLeaf(self):
        if len(self.getChildren()) == 0:
            return True
        else:
            return False

    def getType(self):
        return self.type

    def getIsExit(self):
        return self.isExit
