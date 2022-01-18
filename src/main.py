from BPMNParser import BPMNParser
from Validator import Validator

from src.TranslateAlgorithm import TranslateAlgorithm

if __name__ == '__main__':
    parser = BPMNParser('test.bpmn')
    parser.parse_nodes()
    parser.connect_nodes()
    validator = Validator(parser)
    validator.validate()
    tree = parser.tree.build_tree()

    translator = TranslateAlgorithm()
    result = open('result.txt', 'w')
    print(translator.translate(tree.get_root()), file=result)


