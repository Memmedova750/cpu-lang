# MyCPU-Lang 🚀
A low-level, compiled programming language built from scratch for x86-64 CPU architecture.

## Features
- **Direct CPU Control:** Maps high-level syntax directly to x86-64 registers.
- **Arithmetic Engine:** Supports addition, subtraction, and register-based math.
- **Control Flow:** Implements labels and conditional jumps (Loops & Logic).
- **String Output:** Direct Linux syscall (sys_write) implementation.
- **Variable Abstraction:** Symbol table mapping for human-readable variable names.

## Why I Built This?
This project is part of my journey to understand the deep internals of computer architecture and compiler design. I wanted to see how a simple string like `x = 50` travels from a text file down to the transistors of a CPU.

## How to Run
`python3 src/compiler.py examples/vars.mdil`
Designed and implemented a modular programming language targeting x86-64 Linux.

Features include:

• Recursive Descent Parser
• Abstract Syntax Tree (AST)
• Operator Precedence Parsing
• Symbol Table
• x86-64 Assembly Code Generation
• Linux Syscall Interface
• Stack-based Expression Evaluation
• Automated Build Pipeline