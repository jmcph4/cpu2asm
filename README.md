# cpu2asm #
---

This is an assembler for the [cpu2](https://github.com/jmcph4/cpu2 "cpu2") instruction set architecture, written in Python 3.

## Usage ##
Given some assembly mneumonics

    LDL r01, 0x12
    LDL r02, 0x33
    ADD r03, r01
    ADD r03, r02
    PSH r03
    PSH r02
    PSH r01
    NOP

located in `test.asm`, cpu2asm can be invoked like so:

    python3 cpu2asm test.asm test.bin

This will produce a binary file called `test.bin`, containing machine code for the cpu2 architecture.
