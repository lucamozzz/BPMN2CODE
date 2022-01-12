from BPMNParser import BPMNParser


if __name__ == '__main__':
    parser = BPMNParser('C:\\Users\\alessandro\\Documents\\PycharmProjects-workspace\\BPMN2CODE\\test.bpmn')
    parser.parse_nodes()
    parser.connect_nodes()
    parser.tree.build_tree()



