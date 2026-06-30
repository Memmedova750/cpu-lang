from .ast_nodes import *
from .symbol_table import SymbolTable

class Generator:
    def __init__(self):
        self.strings = []
        self.sym_table = SymbolTable()

    def generate(self, ast):
        func_asm = ""
        for fn in ast.functions:
            # Hər funksiya üçün təzə symbol table (Local Scope)
            local_syms = SymbolTable()
            body_asm = ""
            for node in fn.body:
                body_asm += self.visit(node, local_syms)
            
            # PROLOGUE & EPILOGUE (Full ABI Support)
            stack_size = local_syms.get_stack_size()
            func_asm += f"{fn.name}:\n"
            func_asm += f"    push rbp\n"
            func_asm += f"    mov rbp, rsp\n"
            if stack_size > 0: func_asm += f"    sub rsp, {stack_size}\n"
            
            func_asm += body_asm
            
            func_asm += f"    mov rsp, rbp\n"
            func_asm += f"    pop rbp\n"
            func_asm += "    ret\n"

        main_syms = SymbolTable()
        main_asm = ""
        for node in ast.main_body:
            main_asm += self.visit(node, main_syms)
        
        # Main prologue
        stack_size = main_syms.get_stack_size()
        prologue = "    push rbp\n    mov rbp, rsp\n"
        if stack_size > 0: prologue += f"    sub rsp, {stack_size}\n"

        data_asm = "section .data\n"
        for label, text in self.strings:
            data_asm += f'    {label} db "{text}", 10\n'

        return f"{data_asm}\nsection .text\n    global _start\n\n{func_asm}\n_start:\n{prologue}{main_asm}"

    def visit(self, node, syms):
        if isinstance(node, NumberNode):
            return f"    mov rax, {node.value}\n"
        
        if isinstance(node, BinaryOpNode):
            asm = self.visit(node.right, syms)
            asm += "    push rax\n"
            asm += self.visit(node.left, syms)
            asm += "    pop rbx\n"
            if node.op == '+': asm += "    add rax, rbx\n"
            elif node.op == '-': asm += "    sub rax, rbx\n"
            elif node.op == '*': asm += "    imul rax, rbx\n"
            return asm

        if isinstance(node, AssignmentNode):
            sym = syms.declare(node.name)
            # Dəyişəni Stack-də saxlayırıq: [rbp - offset]
            return self.visit(node.expr, syms) + f"    mov [rbp - {sym['offset']}], rax\n"

        if isinstance(node, ExitNode):
            # Əgər bu bir dəyişəndirsə, onu stack-dən oxu
            sym = syms.lookup(node.expr.value) if isinstance(node.expr, NumberNode) else None
            if sym:
                return f"    mov rdi, [rbp - {sym['offset']}]\n    mov rax, 60\n    syscall\n"
            else:
                return self.visit(node.expr, syms) + "    mov rdi, rax\n    mov rax, 60\n    syscall\n"
        
        if isinstance(node, CallNode):
            asm = ""
            abi_regs = ["rdi", "rsi", "rdx"]
            for i, arg in enumerate(node.args):
                sym = syms.lookup(arg)
                if sym: asm += f"    mov {abi_regs[i]}, [rbp - {sym['offset']}]\n"
                else: asm += f"    mov {abi_regs[i]}, {arg}\n"
            return asm + f"    call {node.name}\n"

        if isinstance(node, PrintNode):
            label = f"str_{len(self.strings)}"
            self.strings.append((label, node.value))
            return f"    mov rax, 1\n    mov rdi, 1\n    mov rsi, {label}\n    mov rdx, {len(node.value)+1}\n    syscall\n"
        
        return ""