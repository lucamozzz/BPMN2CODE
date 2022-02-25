class GestoreAlbero:

    def __init__(self):
        self._trees = list()

    def get_trees(self):
        return self._trees

    def create_tree(self):
        from Tree import Tree
        tree = Tree()
        self._trees.append(tree)
        return Tree()
