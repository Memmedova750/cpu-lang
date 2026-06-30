class Node: pass

class ProgramNode(Node):
    def __init__(self, functions, main_body):
        self.functions = functions
        self.main_body = main_body

class NumberNode(Node):
    def __init__(self, value): self.value = value

class BinaryOpNode(Node):
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

class AssignmentNode(Node):
    def __init__(self, name, expr):
        self.name, self.expr = name, expr

class ExitNode(Node):
    def __init__(self, expr): self.expr = expr

class PrintNode(Node):
    def __init__(self, value): self.value = value

class CallNode(Node):
    def __init__(self, name, args): self.name, self.args = name, args

class FunctionNode(Node):
    def __init__(self, name, body): self.name, self.body = name, body