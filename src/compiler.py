import sys, os, subprocess
from .lexer import Lexer
from .parser import Parser
from .codegen import Generator

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 -m src.compiler <file.mdil>")
        return

    with open(sys.argv[1], "r") as f:
        code = f.read()

    # Pipeline
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse_program()
    
    gen = Generator()
    asm = gen.generate(ast)

    with open("output.asm", "w") as f:
        f.write(asm)
    
    if os.system("nasm -f elf64 output.asm -o output.o && ld output.o -o proqram") == 0:
        print("\n--- [SUCCESS] COMPILATION COMPLETE ---\n")
        res = subprocess.run(["./proqram"])
        print(f"Final CPU Exit Code: {res.returncode}")

if __name__ == "__main__":
    main()