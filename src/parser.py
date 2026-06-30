from .ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self): return self.tokens[self.pos]
    
    def eat(self, kind=None):
        t = self.current()
        self.pos += 1
        return t

    def parse_program(self):
        functions = []
        main_body = []
        while self.current().kind != 'EOF':
            if self.current().value == 'func':
                functions.append(self.parse_function())
            else:
                stmt = self.parse_statement()
                if stmt: main_body.append(stmt)
        return ProgramNode(functions, main_body)

    def parse_function(self):
        self.eat() # func
        name = self.eat().value
        body = []
        while self.current().value != 'end' and self.current().kind != 'EOF':
            stmt = self.parse_statement()
            if stmt: body.append(stmt)
        self.eat() # end
        return FunctionNode(name, body)

    def parse_statement(self):
        t = self.current()
        if t.value == 'set':
            self.eat(); name = self.eat().value; self.eat(); val = self.eat().value
            return AssignmentNode(name, val)
        elif t.value in ['add', 'sub']:
            op = self.eat().value; r1 = self.eat().value; r2 = self.eat().value
            return MathNode(op, r1, r2)
        elif t.value == 'call':
            self.eat(); name = self.eat().value
            args = []
            while self.current().kind in ['NUMBER', 'ID']:
                args.append(self.eat().value)
            return CallNode(name, args)
        elif t.value == 'print':
            self.eat(); return PrintNode(self.eat().value)
        elif t.value == 'exit':
            self.eat(); return ExitNode(self.eat().value)
        self.pos += 1
        return None