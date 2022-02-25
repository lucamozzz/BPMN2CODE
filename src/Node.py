class Node:

    def __init__(self, node_id, type, isExit):
        self.__id = node_id
        self.__parents = list()
        self.__children = list()
        self.__type = type
        self.isExit = isExit

    def getId(self):
        return self.__id

    def getParents(self):
        return self.__parents

    def getChildren(self):
        return self.__children

    def addParent(self, parent):
        self.__parents.append(parent)

    def addChild(self, child):
        self.__children.append(child)

    def addChildIn(self, index, child):
        self.__children.insert(index, child)

    def isLeaf(self):
        if len(self.getChildren()) == 0:
            return True
        else:
            return False

    def getType(self):
        return self.__type

    def getIsExit(self):
        return self.isExit
