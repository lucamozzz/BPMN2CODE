import sys
from BPMNParser import BPMNParser
from TranslateAlgorithm import TranslateAlgorithm
from Validator import Validator

if __name__ == '__main__':
    parser = BPMNParser(sys.argv[1])
    # ™parser = BPMNParser("test.bpmn")
    parser.parse_nodes()
    raw_tree = parser.connect_nodes()
    validator = Validator(parser)
    validator.validate()
    tree = raw_tree.build_tree()
    translator = TranslateAlgorithm()
    print(translator.translate(tree.get_root()))
