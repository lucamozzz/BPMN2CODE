class GestoreAlbero:

    _trees = list()
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def get_trees(self):
        return self._trees

    def create_tree(self):
        from Tree import Tree
        tree = Tree()
        self._trees.append(tree)
        return Tree()
