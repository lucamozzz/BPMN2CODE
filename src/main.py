from BPMNParser import BPMNParser
from src.TranslateAlgorithm import TranslateAlgorithm

if __name__ == '__main__':
    parser = BPMNParser('C:\\Users\\Riccardo\\PycharmProjects\\BPMN2CODE\\test.bpmn')
    parser.parse_nodes()
    parser.connect_nodes()
    tree = parser.tree.build_tree()

    translator = TranslateAlgorithm()
    result = open('C:\\Users\\Riccardo\\PycharmProjects\\BPMN2CODE\\result.txt', 'w')
    print(translator.translate(tree.get_root()), file=result)


