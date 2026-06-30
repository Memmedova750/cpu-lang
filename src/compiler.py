import sys
import os
import subprocess

# Digər modullardan lazımi hissələri import edirik
# Qeyd: Bu faylların hamısının src/ qovluğunda olduğundan əmin ol
from .lexer import Lexer
from .parser import Parser
from .codegen import Generator

def main():
    # 1. Giriş faylının yoxlanılması
    if len(sys.argv) < 2:
        print("\n[ERROR] Usage: python3 -m src.compiler <filename.mdil>")
        return

    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"\n[ERROR] File not found: {input_file}")
        return

    # 2. Mənbə kodun oxunması
    with open(input_file, "r") as f:
        code = f.read()

    try:
        # --- KOMPİLYASİYA PİPELİNE ---

        # Addım A: Lexical Analysis (Mətni tokenlərə çeviririk)
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Addım B: Syntax Analysis (Tokenlərdən AST ağacı qururuq)
        parser = Parser(tokens)
        ast = parser.parse_program()
        
        # Addım C: Code Generation (AST-yə baxıb x86-64 Assembly yazırıq)
        # Bu mərhələdə artıq Stack Frames və Symbol Table idarə olunur
        gen = Generator()
        asm = gen.generate(ast)

        # 3. Assembly kodun fayla yazılması
        with open("output.asm", "w") as f:
            f.write(asm)
        
        print(f"\n[1/3] Assembly generated: output.asm")

        # 4. NASM (Assembler) vasitəsilə maşın koduna (Object file) çevirmə
        nasm_res = os.system("nasm -f elf64 output.asm -o output.o")
        if nasm_res != 0:
            print("[ERROR] NASM compilation failed!")
            return
        print(f"[2/3] Object file created: output.o")

        # 5. LD (Linker) vasitəsilə icra oluna bilən proqram yaratma
        ld_res = os.system("ld output.o -o proqram")
        if ld_res != 0:
            print("[ERROR] Linking failed!")
            return
        print(f"[3/3] Executable created: proqram")

        # --- NƏTİCƏNİN YOXLANILMASI ---
        print("\n" + "="*30)
        print(f"--- RUNNING: {input_file} ---")
        print("="*30)

        # Proqramı işlədirik
        process = subprocess.run(["./proqram"])
        
        # Exit code-u (nəticəni) ekrana çıxarırıq
        print("\n" + "-"*30)
        print(f"FINAL RESULT (CPU Exit Code): {process.returncode}")
        print("-"*30)

    except Exception as e:
        print(f"\n[CRITICAL COMPILER ERROR]:\n{e}")

if __name__ == "__main__":
    main()