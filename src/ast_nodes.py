class Node: pass

class ProgramNode(Node):
    def __init__(self, functions, main_body):
        self.functions = functions
        self.main_body = main_body

class FunctionNode(Node):
    def __init__(self, name, body):
        self.name = name
        self.body = body

class AssignmentNode(Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class MathNode(Node):
    def __init__(self, op, r1, r2):
        self.op = op
        self.r1 = r1
        self.r2 = r2

class CallNode(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class PrintNode(Node):
    def __init__(self, value):
        self.value = value

class ExitNode(Node):
    def __init__(self, value):
        self.value = value