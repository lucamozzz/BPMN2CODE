from src.Tree import Tree

class GestoreAlbero:

    def __init__(self):
        self.trees = list()

    def get_trees(self):
        return self.trees

    def create_tree(self):
        tree = Tree()
        self.trees.append(tree)
        return Tree()
