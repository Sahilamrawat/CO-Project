import re
import sys
import pandas as pd
instructions_dict = {
    # J-type
    "jal": ("1101111", None, None),
    # U-type
    "lui": ("0110111", None, None),
    "auipc": ("0010111", None, None),
    # B-type
    "beq": ("1100011", "000", None),
    "bne": ("1100011", "001", None),
    "blt": ("1100011", "100", None),
    "bge": ("1100011", "101", None),
    "bltu": ("1100011", "110", None),
    "bgeu": ("1100011", "111", None),
    # S-type
    "sw": ("0100011", "010", None),
    # I-type
    "lw": ("0000011", "010", None),
    "addi": ("0010011", "000", None),
    "sltiu": ("0010011", "011", None),
    "jalr": ("1100111", "000", None),
    # R-type
    "add": ("0110011", "000", "0000000"),
    "sub": ("0110011", "000", "0100000"),
    "sll": ("0110011", "001", "0000000"),
    "slt": ("0110011", "010", "0000000"),
    "sltu": ("0110011", "011", "0000000"),
    "xor": ("0110011", "100", "0000000"),
    "srl": ("0110011", "101", "0000000"),
    "or": ("0110011", "110", "0000000"),
    "and": ("0110011", "111", "0000000")
}

registers = {
    "zero": "00000", "ra": "00001", "sp": "00010", "gp": "00011", "tp": "00100",
    "t0": "00101", "t1": "00110", "t2": "00111", "s0": "01000", "s1": "01001",
    "a0": "01010", "a1": "01011", "a2": "01100", "a3": "01101", "a4": "01110",
    "a5": "01111", "a6": "10000", "a7": "10001", "s2": "10010", "s3": "10011",
    "s4": "10100", "s5": "10101", "s6": "10110", "s7": "10111", "s8": "11000",
    "s9": "11001", "s10": "11010", "s11": "11011", "t3": "11100", "t4": "11101",
    "t5": "11110", "t6": "11111"
}


class Assembler:
    def _init_(self, filename):
        self.instructions = []
        with open(filename, "r") as f:
            self.lines = f.readlines()
            self.instructions = [line.strip() for line in self.lines if line]

        self.labels = []
        for i in range(len(self.instructions)):
            if(re.search('\:', self.instructions[i])):
                split = re.split(":", self.instructions[i])
                if(split[0].strip() != split[0]):
                    print("Invalid label at address ", 4 * i)
                    exit()
                self.labels.append([split[0], 4 * i])
                self.instructions[i] = split[1].strip()

        self.asm1 = []
        for i in range(len(self.instructions)):
            self.asm1.append(re.split(" ", self.instructions[i], 1))

    def assemble_instruction(self, instruction, current_address):
        if(instruction[0] not in instructions_dict):
            print("Invalid instruction at address ", current_address)
            exit()
        opcode, funct3, funct7 = instructions_dict[instruction[0]]
        arguments = [arg.strip() for arg in re.split(",|\(|\)|:", instruction[1]) if arg]

        if(len(instruction) != 2):
            print("Invalid instruction at address ", current_address)
            exit()

        if instruction[0] in ["lui", "auipc"]:
            if(len(arguments) != 2):
                print("Invalid instruction at address ", current_address)
                exit()

            if(arguments[0] not in registers):
                print("Invalid register at address ", current_address)
                exit()

            rd = registers[arguments[0]]

            if(int(arguments[1]) >= 2*31 or int(arguments[1]) < -2*31):
                print("Invalid immediate value")
                exit()

            if(int(arguments[1]) >= 0):
                imm = '{:032b}'.format(int(arguments[1]))
            else:
                imm = '{:032b}'.format(2**32 + int(arguments[1]))
            return imm[0:20] + str(rd) + str(opcode)

        # Add other instruction types here

    def assemble(self):
        self.machine_code = []
        for i in range(len(self.instructions)):
            self.current_address = 4 * i
            if self.asm1[i] != [None]:
                assembled_instruction = self.assemble_instruction(self.asm1[i], self.current_address)
                if assembled_instruction is not None:
                    print(f"Address: {self.current_address}, Assembled Instruction: {assembled_instruction}")
                    self.machine_code.append(assembled_instruction)
                else:
                    exit()
        print("Reached assemble method end")
        self.write_to_file("debug_output.txt")  # Debug: Write debug output to a file



    def write_to_file(self, filename):
        with open(filename, "w") as f:
            for i in range(len(self.machine_code)-1):
                if self.machine_code[i] is not None:
                    f.write(self.machine_code[i] + "\n")
                    print("Writing to file:", self.machine_code[i])
                else:
                    f.write("\n")
            if self.machine_code[-1] is not None:
                f.write(self.machine_code[-1])
                print("Writing to file:", self.machine_code[-1])




if _name_ =="_main_":
    
    input_file = r'C:\Users\kumar\OneDrive\Desktop\cd\test.txt'
    output_file = 'output.txt'
    assembler = Assembler(input_file)
    assembler.assemble()
    assembler.write_to_file(output_file)
    print("Done")