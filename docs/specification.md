# MənimDil (MyLang) Spesifikasiyası - Versiya 0.1

## Məqsəd
x86-64 CPU arxitekturası üçün aşağı səviyyəli (low-level) və sürətli proqramlaşdırma dili yaratmaq.

## Dilin İlk Qaydaları (Syntax)
1. **Dəyişən təyin etmək:** 
   `dəyişən x = 10`
   
2. **Riyazi əməliyyatlar:**
   `topla 5, 10`
   
3. **Proqramı bitirmək (Exit):**
   `bitir 0` (Bu, birbaşa CPU-ya 'exit syscall' göndərəcək)

## Hədəf Arxitektura
- CPU: x86-64
- OS: Linux (WSL2 üzərindən)
- Assembler: NASM