class SymbolTable:
    def __init__(self):
        self.symbols = {} # name -> {offset, type}
        self.stack_offset = 0

    def declare(self, name, sym_type="int"):
        if name not in self.symbols:
            self.stack_offset += 8 # Hər dəyişən üçün 8 bayt yer ayırırıq
            self.symbols[name] = {"offset": self.stack_offset, "type": sym_type}
        return self.symbols[name]

    def lookup(self, name):
        return self.symbols.get(name)

    def get_stack_size(self):
        # Yaddaşda ayrılacaq cəmi yer (16-ya bölünən olmalıdır - Stack Alignment)
        return (self.stack_offset + 15) & ~15