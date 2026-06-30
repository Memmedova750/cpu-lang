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

    # 1. Primary: Rəqəm və ya ( İfadə )
    def parse_primary(self):
        t = self.current()
        if t.kind == 'NUMBER':
            return NumberNode(self.eat().value)
        elif t.value == '(':
            self.eat() # (
            expr = self.parse_expression()
            self.eat() # )
            return expr
        elif t.kind == 'ID':
            return NumberNode(self.eat().value) # Hələlik bəsit saxlayaq
        return None

    # 2. Term: Vurma və Bölmə
    def parse_term(self):
        node = self.parse_primary()
        while self.current().value in ['*', '/']:
            op = self.eat().value
            right = self.parse_primary()
            node = BinaryOpNode(node, op, right)
        return node

    # 3. Expression: Toplama və Çıxma
    def parse_expression(self):
        node = self.parse_term()
        while self.current().value in ['+', '-']:
            op = self.eat().value
            right = self.parse_term()
            node = BinaryOpNode(node, op, right)
        return node

    def parse_program(self):
        functions, main_body = [], []
        while self.current().kind != 'EOF':
            if self.current().value == 'func':
                functions.append(self.parse_function())
            else:
                stmt = self.parse_statement()
                if stmt: main_body.append(stmt)
        return ProgramNode(functions, main_body)

    def parse_function(self):
        self.eat(); name = self.eat().value
        body = []
        while self.current().value != 'end':
            body.append(self.parse_statement())
        self.eat(); return FunctionNode(name, body)

    def parse_statement(self):
        t = self.current()
        if t.value == 'set':
            self.eat(); name = self.eat().value; self.eat(); expr = self.parse_expression()
            return AssignmentNode(name, expr)
        elif t.value == 'exit':
            self.eat(); return ExitNode(self.parse_expression())
        elif t.value == 'print':
            self.eat(); return PrintNode(self.eat().value)
        elif t.value == 'call':
            self.eat(); name = self.eat().value
            args = []
            while self.current().kind in ['NUMBER', 'ID']: args.append(self.eat().value)
            return CallNode(name, args)
        self.pos += 1
        return None