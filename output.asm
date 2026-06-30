section .data

section .text
    global _start

my_math_logic:
    add rdi, rsi
    mov rdi, rdi
    mov rax, 60
    syscall
    ret

_start:
    mov rdi, 10
    mov rsi, 20
    call my_math_logic
