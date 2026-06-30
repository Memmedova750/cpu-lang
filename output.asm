section .data
    str_0 db "ADIN_NEDIR?", 10
    str_1 db "SALAM", 10

section .bss
    ad resb 64

section .text
    global _start

_start:
    mov rax, 1
    mov rdi, 1
    mov rsi, str_0
    mov rdx, 12
    syscall
    mov rax, 0
    mov rdi, 0
    mov rsi, ad
    mov rdx, 64
    syscall
    mov rax, 1
    mov rdi, 1
    mov rsi, str_1
    mov rdx, 6
    syscall
    mov rax, 1
    mov rdi, 1
    mov rsi, ad
    mov rdx, 64
    syscall
    mov rdi, 0
    mov rax, 60
    syscall
