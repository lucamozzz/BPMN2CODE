from BPMNParser import BPMNParser
from Validator import Validator


if __name__ == '__main__':
    #TODO Cambiare percorso file .bpmn con argomento in input
    parser = BPMNParser('C:\\Users\\alessandro\\Documents\\PycharmProjects-workspace\\BPMN2CODE\\test.bpmn')
    parser.parse_nodes()
    parser.connect_nodes()
    parser.tree.build_tree()
    validator = Validator(parser)
    validator.validate()
