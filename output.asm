section .data

section .text
    global _start


_start:
    push rbp
    mov rbp, rsp
    sub rsp, 16
    mov rax, 2
    push rax
    mov rax, 5
    push rax
    mov rax, 10
    pop rbx
    add rax, rbx
    pop rbx
    imul rax, rbx
    mov [rbp - 8], rax
    mov rdi, [rbp - 8]
    mov rax, 60
    syscall
