from BPMNParser import BPMNParser


# This class is intended to make sure that the BPMN model given
# by the user is actually following the bounds we imposed
class Validator:

    def __init__(self, source: BPMNParser):
        self.__source = source

    def validate(self):
        self.__check_start_end()
        self.__check_gateway_balance()
        self.__check_annotations()
        self.__check_conditions()
        self.__check_single_entrance()
        self.__check_single_exit()

    # Checks if there is more than one StartEvent
    # as well as EndEvents
    def __check_start_end(self):
        nodes = self.__source.getNodes()
        s, e = 0, 0
        for node in nodes:
            if node.getType() == 'StartEvent':
                s = s + 1
            elif node.getType() == 'EndEvent':
                e = e + 1
            else:
                continue
        if s != 1:
            print("Either too many 'StartEvents' in your BPMN model or none: ({})".format(s))
        if e != 1:
            print("Either too many 'EndEvents' in your BPMN model or none: ({})".format(e))

    # Checks if opened gateways get closed
    def __check_gateway_balance(self):
        nodes = self.__source.getNodes()
        e = 0
        i = 0
        for node in nodes:
            if node.getType() == 'ExclusiveGateway' or node.getType() == 'ParallelGateway':
                if node.getIsExit():
                    e = e - 1
                else:
                    e = e + 1
        if i < 0:
            print("Found ({}) closing gateway(s) without a opening gateway".format(e))
        if i > 0:
            print("Found ({}) opening gateway(s) without a closing gateway".format(e))

    # Checks if text annotations contain something different
    # than 'exit' or 'loop' keywords
    def __check_annotations(self):
        annotations = self.__source.getAnnotations()
        for ann in annotations:
            value = ann.getValue()
            if value != 'exit' and value != 'loop':
                e = ann.getValue()
                print("Annotations MUST contain only 'loop' or 'exit'. Found ({}) instead.".format(e))

    # Checks if exclusive gateways define a condition
    def __check_conditions(self):
        nodes = self.__source.getNodes()
        i = 0
        for node in nodes:
            if node.getType() == 'ExclusiveGateway':
                if not node.getIsExit():
                    for con in self.__source.getConnections():
                        if con.attrib['sourceRef'] == node.getId():
                            if node.getCondition == '':
                                i = i + 1
        if i > 0:
            print("({}) exclusive gateway(s) missing condition. Please define one.".format(i))

    # Checks if a block has a single way in
    def __check_single_entrance(self):
        nodes = self.__source.getNodes()
        i = 0
        a = 0
        for node in nodes:
            if node.getType() == 'ExclusiveGateway' or node.getType() == 'ParallelGateway':
                if not node.getIsExit():
                    for s in self.__source.getSequenceFlows():
                        if s.get('targetRef') == node.getId():
                            i = i + 1
                    if a > 1:
                        if not node.getLoop():
                            print("Found an opening gateway with more than one entrance or none.")
                    i = 0

    # Checks if a block has a single way out
    def __check_single_exit(self):
        nodes = self.__source.getNodes()
        i = 0
        for node in nodes:
            if node.getType() == 'ExclusiveGateway' or node.getType() == 'ParallelGateway':
                if node.getIsExit():
                    for s in self.__source.getSequenceFlows():
                        if s.get('sourceRef') == node.getId():
                            i = i + 1
                    if i > 1:
                        if not node.getLoop():
                            print("Found a closing gateway with more than one exit or none.")
                    i = 0