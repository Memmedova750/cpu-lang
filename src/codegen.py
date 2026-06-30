from .ast_nodes import *

class Generator:
    def __init__(self):
        self.strings = []
        self.symbols = {
            "x": "r8", "y": "r9", "z": "r10",
            "rdi": "rdi", "rsi": "rsi", "rdx": "rdx", "rax": "rax"
        }

    def generate(self, ast):
        # 1. Funksiyaları emal et
        func_asm = ""
        for fn in ast.functions:
            func_asm += f"{fn.name}:\n"
            for node in fn.body: func_asm += self.visit(node)
            func_asm += "    ret\n"

        # 2. Əsas proqramı emal et
        main_asm = ""
        for node in ast.main_body: main_asm += self.visit(node)

        # 3. Data bölməsini yarat
        data_asm = "section .data\n"
        for label, text in self.strings:
            data_asm += f'    {label} db "{text}", 10\n'

        return f"{data_asm}\nsection .text\n    global _start\n\n{func_asm}\n_start:\n{main_asm}"

    def visit(self, node):
        if isinstance(node, AssignmentNode):
            reg = self.symbols.get(node.name, "rax")
            return f"    mov {reg}, {node.value}\n"
        
        elif isinstance(node, MathNode):
            r1 = self.symbols.get(node.r1, node.r1)
            r2 = self.symbols.get(node.r2, node.r2)
            return f"    {node.op} {r1}, {r2}\n"
        
        elif isinstance(node, CallNode):
            asm = ""
            abi_regs = ["rdi", "rsi", "rdx", "rcx"]
            for i, arg in enumerate(node.args):
                val = self.symbols.get(arg, arg)
                asm += f"    mov {abi_regs[i]}, {val}\n"
            return asm + f"    call {node.name}\n"
        
        elif isinstance(node, PrintNode):
            label = f"str_{len(self.strings)}"
            self.strings.append((label, node.value))
            return f"    mov rax, 1\n    mov rdi, 1\n    mov rsi, {label}\n    mov rdx, {len(node.value)+2}\n    syscall\n"
        
        elif isinstance(node, ExitNode):
            val = self.symbols.get(node.value, node.value)
            return f"    mov rdi, {val}\n    mov rax, 60\n    syscall\n"
        return ""