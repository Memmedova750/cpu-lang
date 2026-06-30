import re

class Token:
    def __init__(self, kind, value, line):
        self.kind = kind
        self.value = value
        self.line = line
    def __repr__(self):
        return f"Token({self.kind}, {self.value}, {self.line})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.spec = [
            ('NUMBER',   r'\d+'),
            ('ID',       r'\b[A-Za-z_][A-Za-z0-9_]*\b'),
            ('STRING',   r'"[^"]*"'),
            ('OP',       r'[=\+\-\*/]'),
            ('NEWLINE',  r'\n'),
            ('SKIP',     r'[ \t\r]+'),
        ]

    def tokenize(self):
        tokens = []
        line_num = 1
        tok_regex = '|'.join('(?P<%s>%s)' % p for p in self.spec)
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'NEWLINE': line_num += 1; continue
            if kind == 'SKIP': continue
            if kind == 'STRING': value = value[1:-1]
            tokens.append(Token(kind, value, line_num))
        tokens.append(Token('EOF', None, line_num))
        return tokens