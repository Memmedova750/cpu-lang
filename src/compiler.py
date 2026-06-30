import sys, os, subprocess

def main():
    if len(sys.argv) < 2: return
    input_file = sys.argv[1]
    with open(input_file, "r") as f: lines = f.readlines()

    # Dəyişənləri registrlərə eşidən cədvəl (Simvol Cədvəli)
    # Hələlik sadə olsun deyə: x -> rax, y -> rbx, z -> rcx
    simvollar = {"x": "rax", "y": "rbx", "z": "rcx"}
    
    asm_body = ""
    for line in lines:
        line = line.strip()
        if not line: continue
        parts = line.split()
        cmd = parts[0]

        # dəyişən x = 50
        if cmd == "dəyişən":
            ad = parts[1]
            deyer = parts[3] # '=' işarəsini keçirik
            reg = simvollar[ad]
            asm_body += f"    mov {reg}, {deyer}\n"

        # topla x y
        if cmd == "topla":
            reg1 = simvollar[parts[1]]
            reg2 = simvollar[parts[2]]
            asm_body += f"    add {reg1}, {reg2}\n"

        # bitir x
        if cmd == "bitir":
            reg = simvollar.get(parts[1], parts[1]) # Əgər rəqəmdirsə rəqəmi, dəyişəndirsə registri götür
            asm_body += f"    mov rdi, {reg}\n    mov rax, 60\n    syscall\n"

    final_asm = f"section .text\n    global _start\n\n_start:\n{asm_body}"
    with open("output.asm", "w") as f: f.write(final_asm)
    
    os.system("nasm -f elf64 output.asm -o output.o")
    os.system("ld output.o -o proqram")
    
    print("--- DƏYİŞƏN TESTİ İŞLƏYİR ---")
    res = subprocess.run(["./proqram"])
    print(f"Nəticə: {res.returncode}")

if __name__ == "__main__":
    main()