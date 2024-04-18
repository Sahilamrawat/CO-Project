registers = open("CO PROJECT\\regs.txt", "r").read()
registers = eval(registers)

output = open("CO PROJECT\\output.txt", 'w+')

from vars import *

memory = open("CO PROJECT\\memory.txt", 'r').read()
memory = eval(memory)

def binarytodecimal(num, type='unsigned'):
    if type == 'signed':
        if num[0] == '1':
            s = 0
            s = s - (2)**(len(num)-1)
            for i in range(1, len(num)):
                s = s + int(num[i])*(2**(len(num)-i-1))
            return s
        if num[0] == '0':
            s = 0
            for i in range(1, len(num)):
                s = s + int(num[i])*(2**(len(num)-i-1))
            return s
    else:
        s = 0
        for i in range(0, len(num)):
            s = s + int(num[i])*(2**(len(num)-i-1))
        return s
        
def signextend(digit, num, size=32):
    if len(bin(num)[2:]) > size:
        raise OverflowError('Error: Illegal immediate overflow')
    return digit*(size-len(bin(num)[2:])) + bin(num)[2:]

def decimaltobinary(num, type='unsigned', size=32):
    global output
    if type == 'signed':
        if num < 0:
            number = '0' + bin(abs(num))[2:]
            new = ''
            for i in number:
                if i == '0':
                    new = new + '1'
                else:
                    new = new + '0'
            onescomplement = int(new, 2)
            twoscomplement = onescomplement + 1
            return signextend('1', twoscomplement, size)
        if num >= 0:
            twoscomplement = num
            return signextend('0', twoscomplement, size)
    if type == 'unsigned':
        if num < 0:
            raise OverflowError('Error: Illegal immediate overflow')
        nums = num
        return signextend('0', nums, size)

class simulator:
    def execution(self, line):
        if line[-7:] == '0110011' and line[:7] == '0100000' and line[17:20] == '000':
            self.sub(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '000':
            self.add(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '001':
            self.sll(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '010':
            self.slt(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '011':
            self.sltu(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '100':
            self.xor(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '101':
            self.srl(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '110':
            self.OR(line)
            return
        elif line[-7:] == '0110011' and line[17:20] == '111':
            self.AND(line)
            return
        elif line[-7:] == '0000011' and line[17:20] == '010':
            self.lw(line)
            return
        elif line[-7:] == '0010011' and line[17:20] == '000':
            self.addi(line)
            return
        elif line[-7:] == '0010011' and line[17:20] == '011':
            self.sltiu(line)
            return
        elif line[-7:] == '1100111' and line[17:20] == '000':
            self.jalr(line)
            return
        elif line[-7:] == '0100011' and line[17:20] == '010':
            self.sw(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '000':
            self.beq(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '001':
            self.bne(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '100':
            self.blt(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '101':
            self.bge(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '110':
            self.bgeu(line)
            return
        elif line[-7:] == '1100011' and line[17:20] == '111':
            self.bltu(line)
            return
        elif line[-7:] == '0110111':
            self.lui(line)
            return
        elif line[-7:] == '0010111':
            self.auipc(line)
            return
        elif line[-7:] == '1101111':
            self.jal(line)
            return
        elif line[-7:] == '1110001' and line[17:20] == '000':
            self.mul(line)
            return
        elif line[-7:] == '1110001' and line[17:20] == '001':
            self.rst(line)
            return
        elif line[-7:] == '1110001' and line[17:20] == '010':
            self.halt(line)
            return
        elif line[-7:] == '1110001' and line[17:20] == '011':
            self.rvrs(line)
            return
    
    def add(self, line):
        src_reg1 = registers[line[12:17]]
        src_reg2 = registers[line[7:12]]
        dest_reg = registers[line[20:25]]

        value1 = binarytodecimal(globals()[src_reg1], 'signed')
        value2 = binarytodecimal(globals()[src_reg2], 'signed')
        result = decimaltobinary(value1 + value2, 'signed')

        globals()[dest_reg] = result
        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4

        
    def sub(self, line):
        src_reg1 = registers[line[12:17]]
        src_reg2 = registers[line[7:12]]
        dest_reg = registers[line[20:25]]

        value1 = binarytodecimal(globals()[src_reg1], 'signed')
        value2 = binarytodecimal(globals()[src_reg2], 'signed')
        result = decimaltobinary(value1 - value2, 'signed')

        globals()[dest_reg] = result
        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4

        
    def sll(self, line):
        shift_amount = binarytodecimal(globals()[registers[line[7:12]]][-5:])
        src_reg = registers[line[12:17]]
        dest_reg = registers[line[20:25]]

        src_value = binarytodecimal(globals()[src_reg], 'signed')
        result = decimaltobinary(src_value << shift_amount, 'signed')

        globals()[dest_reg] = result
        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4


    def slt(self, line):
        src_reg1 = registers[line[7:12]]
        src_reg2 = registers[line[12:17]]
        dest_reg = registers[line[20:25]]

        value1 = binarytodecimal(globals()[src_reg1], 'signed')
        value2 = binarytodecimal(globals()[src_reg2], 'signed')

        if value1 < value2:
            globals()[dest_reg] = decimaltobinary(1, 'signed')
        else:
            globals()[dest_reg] = decimaltobinary(0, 'signed')

        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4


        
    def sltu(self, line):
        src_reg1 = registers[line[7:12]]
        src_reg2 = registers[line[12:17]]
        dest_reg = registers[line[20:25]]

        value1 = binarytodecimal(globals()[src_reg1])
        value2 = binarytodecimal(globals()[src_reg2])

        if value1 < value2:
            globals()[dest_reg] = decimaltobinary(1, 'signed')
        else:
            globals()[dest_reg] = decimaltobinary(0, 'signed')

        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4

        
    def srl(self, line):
        shift_amount = binarytodecimal(globals()[registers[line[7:12]]][-5:])
        src_reg = registers[line[12:17]]
        dest_reg = registers[line[20:25]]

        src_value = binarytodecimal(globals()[src_reg], 'signed')
        result = decimaltobinary(src_value >> shift_amount, 'signed')

        globals()[dest_reg] = result
        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4


        
    def OR(self, line):
        src_reg1 = registers[line[7:12]]
        src_reg2 = registers[line[12:17]]
        dest_reg = registers[line[20:25]]

        value1 = binarytodecimal(globals()[src_reg1], 'signed')
        value2 = binarytodecimal(globals()[src_reg2], 'signed')
        result = decimaltobinary(value1 | value2, 'signed')

        globals()[dest_reg] = result
        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4
        
    def AND(self, line):
        src_reg1 = registers[line[7:12]]
        src_reg2 = registers[line[12:17]]
        dest_reg = registers[line[20:25]]

        value1 = binarytodecimal(globals()[src_reg1], 'signed')
        value2 = binarytodecimal(globals()[src_reg2], 'signed')
        result = decimaltobinary(value1 & value2, 'signed')

        globals()[dest_reg] = result
        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4

    def lw(self, line):
        dest_reg = registers[line[20:25]]
        base_reg = registers[line[12:17]]
        offset = binarytodecimal(line[:12], 'signed')
        
        address = binarytodecimal(globals()[base_reg], 'signed') + offset
        globals()[dest_reg] = memory[address]

        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4

        
    def addi(self, line):
        dest_reg = registers[line[20:25]]
        base_reg = registers[line[12:17]]
        imm_value = binarytodecimal(line[:12], 'signed')
        
        base_value = binarytodecimal(globals()[base_reg], 'signed')
        result = decimaltobinary(base_value + imm_value, 'signed')

        globals()[dest_reg] = result
        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4
    
    def sltiu(self, line):
        src_reg = registers[line[12:17]]
        imm_value = binarytodecimal(line[:12], 'signed')

        if binarytodecimal(globals()[src_reg], 'signed') < imm_value:
            globals()[registers[line[20:25]]] = decimaltobinary(1, 'signed')
        else:
            globals()[registers[line[20:25]]] = '0' * 32

        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        globals()['pc'] += 4

    def jalr(self, line):
        dest_reg = registers[line[20:25]]
        src_reg = registers[line[12:17]]
        imm_value = binarytodecimal(line[:12], 'signed')

        globals()[dest_reg] = decimaltobinary(globals()['pc'] + 4, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        globals()['pc'] = (binarytodecimal(globals()[src_reg], 'signed') + imm_value) & ~1

        output_line = '0b' + decimaltobinary(globals()['pc'] - 4, 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)     

    def sw(self, line):
        mem_address = binarytodecimal(globals()[registers[line[12:17]]], 'signed') + binarytodecimal(line[:7] + line[20:25], 'signed')
        memory[mem_address] = globals()[registers[line[7:12]]]
        
        globals()['zero'] = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        
        globals()['pc'] += 4

    def bne(self, line):
        globals()['zero'] = '00000000000000000000000000000000'
        
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') != binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
            
          
    
    def beq(self, line):
        zero_register = '00000000000000000000000000000000'
        dest_reg = registers[line[20:25]]
        src_reg1 = registers[line[12:17]]
        src_reg2 = registers[line[7:12]]
        
        if binarytodecimal(globals()[src_reg1], 'signed') == binarytodecimal(globals()[src_reg2], 'signed'):
            imm_value = binarytodecimal(line[0] + line[-8] + line[1:7] + line[-12:-8] + '0', 'signed')
            globals()['pc'] += imm_value
            output_line = '0b' + decimaltobinary(globals()['pc'] - 4, 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
            output.write(output_line)
        else:
            output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
            output.write(output_line)
        
        globals()['pc'] += 4
    
    
    def blt(self, line):
        
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') < binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4

    def bge(self, line):
        zero_register = '00000000000000000000000000000000'
        dest_reg = registers[line[20:25]]
        src_reg1 = registers[line[12:17]]
        src_reg2 = registers[line[7:12]]
        
        if binarytodecimal(globals()[src_reg1], 'signed') > binarytodecimal(globals()[src_reg2], 'signed'):
            imm_value = binarytodecimal(line[0] + line[-8] + line[1:7] + line[-12:-8] + '0', 'signed')
            globals()['pc'] += imm_value
            output_line = '0b' + decimaltobinary(globals()['pc'] - 4, 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
            output.write(output_line)
        else:
            output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
            output.write(output_line)
        
        globals()['pc'] += 4

    def bltu(self, line):
        zero_register = '00000000000000000000000000000000'
        dest_reg = registers[line[20:25]]
        src_reg1 = registers[line[12:17]]
        src_reg2 = registers[line[7:12]]
        
        if binarytodecimal(globals()[src_reg1]) < binarytodecimal(globals()[src_reg2]):
            imm_value = binarytodecimal(line[0] + line[-8] + line[1:7] + line[-12:-8] + '0', 'signed')
            globals()['pc'] += imm_value
            output_line = '0b' + decimaltobinary(globals()['pc'] - 4, 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
            output.write(output_line)
        else:
            output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
            output.write(output_line)
        
        globals()['pc'] += 4

    
    def bgeu(self, line):
        zero_register = '00000000000000000000000000000000'
        dest_reg = registers[line[20:25]]
        src_reg1 = registers[line[12:17]]
        src_reg2 = registers[line[7:12]]
        
        if binarytodecimal(globals()[src_reg1]) > binarytodecimal(globals()[src_reg2]):
            imm_value = binarytodecimal(line[0] + line[-8] + line[1:7] + line[-12:-8] + '0', 'signed')
            globals()['pc'] += imm_value
            output_line = '0b' + decimaltobinary(globals()['pc'] - 4, 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
            output.write(output_line)
        else:
            output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
            output.write(output_line)
        
        globals()['pc'] += 4
    
    def auipc(self, line):
        zero_register = '00000000000000000000000000000000'
        dest_reg = registers[line[20:25]]
        imm_value = binarytodecimal(line[:20] + '000000000000', 'signed')
        
        globals()[dest_reg] = decimaltobinary(globals()['pc'] + imm_value, 'signed')
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        
        globals()['pc'] += 4
        
    def lui(self, line):
        dest_reg = registers[line[20:25]]
        imm_value = line[:20] + '000000000000'
        
        globals()[dest_reg] = imm_value
        zero_register = '00000000000000000000000000000000'
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
        
        globals()['pc'] += 4

    def jal(self, line):
        # Calculate the target address
        target_address = globals()['pc'] + 4 + (binarytodecimal(line[0] + line[12:20] + line[11] + line[1:11] + '0', 'signed')) & ~1
        
        # Update the return address in the destination register
        globals()[registers[line[20:25]]] = decimaltobinary(globals()['pc'] + 4, 'signed')
        
        # Update the program counter
        globals()['pc'] = target_address
        
        # Write the output line
        output_line = '0b' + decimaltobinary(globals()['pc'] - 4, 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)
    
    def mul(self, line):
        # Increment the program counter
        globals()['pc'] += 4
        
        # Calculate the result of the multiplication
        result = binarytodecimal(globals()[registers[line[12:17]]], 'signed') * binarytodecimal(globals()[registers[line[7:12]]], 'signed')
        
        # Update the destination register with the result
        globals()[registers[line[20:25]]] = decimaltobinary(result, 'signed')
        
        # Write the output line
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)

    def rst(self, line):
        globals()['pc'] += 4
        globals()['zero'] = '00000000000000000000000000000000'
        globals()['ra'] = '00000000000000000000000000000000'
        globals()['sp'] = '00000000000000000000000000000000'
        globals()['gp'] = '00000000000000000000000000000000'
        globals()['tp'] = '00000000000000000000000000000000'
        globals()['t0'] = '00000000000000000000000000000000'
        globals()['t1'] = '00000000000000000000000000000000'
        globals()['t2'] = '00000000000000000000000000000000'
        globals()['s0'] = '00000000000000000000000000000000'
        globals()['s1'] = '00000000000000000000000000000000'
        globals()['a0'] = '00000000000000000000000000000000'
        globals()['a1'] = '00000000000000000000000000000000'
        globals()['a2'], globals()['a3'], globals()['a4'], globals()['a5'], globals()['a6'], globals()['a7'] = '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000'
        globals()['s2'] = '00000000000000000000000000000000'
        globals()['s3'] = '00000000000000000000000000000000'
        globals()['s4'] = '00000000000000000000000000000000'
        globals()['s5'] = '00000000000000000000000000000000'
        globals()['s6'] = '00000000000000000000000000000000'
        globals()['s7'] = '00000000000000000000000000000000'
        globals()['s8'] = '00000000000000000000000000000000'
        globals()['s9'] = '00000000000000000000000000000000'
        globals()['s10'] = '00000000000000000000000000000000'
        globals()['s11'] = '00000000000000000000000000000000'
        globals()['t3'], globals()['t4'], globals()['t5'], globals()['t6'] = '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
    
    def rvrs(self, line):
        # Increment the program counter
        globals()['pc'] += 4
        
        # Reverse the contents of the source register and store it in the destination register
        src_reg = registers[line[12:17]]
        dest_reg = registers[line[20:25]]
        globals()[dest_reg] = globals()[src_reg][::-1]
        
        # Write the output line
        output_line = '0b' + decimaltobinary(globals()['pc'], 'signed') + ' ' + ' '.join(['0b' + globals()[reg] for reg in registers.values()]) + '\n'
        output.write(output_line)

        
        
        
input_file = open("CO PROJECT\\text.txt", 'r')

l = input_file.readlines()

l = [i.strip('\n') for i in l]

x = simulator()

while int(pc//4)-1 < len(l):
    if l[int(pc//4)-1] == '00000000000000000000000001100011':
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        break
    if l[int(pc//4)-1] == '00000000000000000010000001110001':
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        break
    x.execution(l[int(pc//4)-1])
    
for i in memory:
    output.write('0x000'+hex(i)[2:]+':'+'0b'+memory[i]+'\n')


output.close()