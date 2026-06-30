import sys, os, subprocess

def compile_line(line, strings, buffers):
    line = line.strip()
    if not line or line.startswith(";"): return ""
    parts = line.split()
    cmd = parts[0]

    # PRINT "HELLO"
    if cmd == "print":
        if parts[1] in buffers:
            return f"    mov rax, 1\n    mov rdi, 1\n    mov rsi, {parts[1]}\n    mov rdx, 64\n    syscall"
        else:
            text = parts[1]
            str_name = f"str_{len(strings)}"
            strings.append((str_name, text))
            return f"    mov rax, 1\n    mov rdi, 1\n    mov rsi, {str_name}\n    mov rdx, {len(text) + 1}\n    syscall"

    # READ name
    if cmd == "read":
        buf_name = parts[1]
        buffers.append(buf_name)
        return f"    mov rax, 0\n    mov rdi, 0\n    mov rsi, {buf_name}\n    mov rdx, 64\n    syscall"

    # SET rax 10
    if cmd == "set":
        return f"    mov {parts[1]}, {parts[2]}"

    # ADD rax 5
    if cmd == "add":
        return f"    add {parts[1]}, {parts[2]}"

    # SUB rax 1
    if cmd == "sub":
        return f"    sub {parts[1]}, {parts[2]}"

    # COMPARE rax 10
    if cmd == "compare":
        return f"    cmp {parts[1]}, {parts[2]}"

    # JUMP_IF_EQUAL label_name
    if cmd == "jump_eq":
        return f"    je {parts[1]}"

    # LABEL loop_start
    if cmd == "label":
        return f"{parts[1]}:"

    # EXIT 0
    if cmd == "exit":
        return f"    mov rdi, {parts[1]}\n    mov rax, 60\n    syscall"
    
    return f"; {line}"

def main():
    if len(sys.argv) < 2: return
    input_file = sys.argv[1]
    with open(input_file, "r") as f: lines = f.readlines()

    strings, buffers = [], []
    asm_body = ""
    for line in lines:
        asm_body += compile_line(line, strings, buffers) + "\n"

    asm_data = "section .data\n"
    for name, text in strings:
        asm_data += f'    {name} db "{text}", 10\n'

    asm_bss = "section .bss\n"
    for name in buffers:
        asm_bss += f"    {name} resb 64\n"

    final_asm = f"{asm_data}\n{asm_bss}\nsection .text\n    global _start\n\n_start:\n{asm_body}"
    
    with open("output.asm", "w") as f: f.write(final_asm)
    
    os.system("nasm -f elf64 output.asm -o output.o")
    os.system("ld output.o -o proqram")
    
    print(f"--- Global Compilation of '{input_file}' Successful ---\n")
    os.system("./proqram")

if __name__ == "__main__":
    main()