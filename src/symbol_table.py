class SymbolTable:
    def __init__(self):
        self.symbols = {} # name -> {type, reg, scope, etc.}
        self.regs = ["r8", "r9", "r10", "r11", "r12"]
        self.counter = 0

    def define(self, name, sym_type="int"):
        if name not in self.symbols:
            reg = self.regs[self.counter % len(self.regs)]
            self.symbols[name] = {"type": sym_type, "reg": reg}
            self.counter += 1
        return self.symbols[name]

    def lookup(self, name):
        return self.symbols.get(name)