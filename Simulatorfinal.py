registers = {'00000': 'zero', '00001': 'ra', '00010': 'sp', '00011': 'gp', '00100': 'tp', '00101': 't0', '00110': 't1', '00111': 't2',
             '01000': 's0', '01001': 's1', '01010': 'a0', '01011': 'a1', '01100': 'a2', '01101': 'a3', 
             '01110': 'a4', '01111': 'a5', '10000': 'a6', '10001': 'a7', '10010': 's2', '10011': 's3', '10100': 's4', 
             '10101': 's5', '10110': 's6', '10111': 's7', '11000': 's8', '11001': 's9', '11010': 's10', '11011': 's11', 
             '11100': 't3', '11101': 't4', '11110': 't5', '11111': 't6'
}

output = open("C:\\Users\\kumar\\OneDrive\\Desktop\\output.txt", 'w+')


zero = '00000000000000000000000000000000'
ra = '00000000000000000000000000000000'
sp = '00000000000000000000000100000000'
gp = '00000000000000000000000000000000'
tp = '00000000000000000000000000000000'
t0 = '00000000000000000000000000000000'
t1 = '00000000000000000000000000000000'
t2 = '00000000000000000000000000000000'
s0 = '00000000000000000000000000000000'
s1 = '00000000000000000000000000000000'
a0 = '00000000000000000000000000000000'
a1 = '00000000000000000000000000000000'
a2, a3, a4, a5, a6, a7 = '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000'
s2 = '00000000000000000000000000000000'
s3 = '00000000000000000000000000000000'
s4 = '00000000000000000000000000000000'
s5 = '00000000000000000000000000000000'
s6 = '00000000000000000000000000000000'
s7 = '00000000000000000000000000000000'
s8 = '00000000000000000000000000000000'
s9 = '00000000000000000000000000000000'
s10 = '00000000000000000000000000000000'
s11 = '00000000000000000000000000000000'
t3, t4, t5, t6 = '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000', '00000000000000000000000000000000'
pc = 4

memory = {
    65536: '00000000000000000000000000000000', 65540: '00000000000000000000000000000000', 65544: '00000000000000000000000000000000',
    65548: '00000000000000000000000000000000', 65552: '00000000000000000000000000000000', 65556: '00000000000000000000000000000000',
    65560: '00000000000000000000000000000000', 65564: '00000000000000000000000000000000', 65568: '00000000000000000000000000000000',
    65572: '00000000000000000000000000000000', 65576: '00000000000000000000000000000000', 65580: '00000000000000000000000000000000',
    65584: '00000000000000000000000000000000', 65588: '00000000000000000000000000000000', 65592: '00000000000000000000000000000000',
    65596: '00000000000000000000000000000000', 65600: '00000000000000000000000000000000', 65604: '00000000000000000000000000000000',
    65608: '00000000000000000000000000000000', 65612: '00000000000000000000000000000000', 65616: '00000000000000000000000000000000',
    65620: '00000000000000000000000000000000', 65624: '00000000000000000000000000000000', 65628: '00000000000000000000000000000000',
    65632: '00000000000000000000000000000000', 65636: '00000000000000000000000000000000', 65640: '00000000000000000000000000000000',
    65644: '00000000000000000000000000000000', 65648: '00000000000000000000000000000000', 65652: '00000000000000000000000000000000',
    65656: '00000000000000000000000000000000', 65660: '00000000000000000000000000000000'
}

def binarytodecimal(num, type='unsigned'):
    if isinstance(num, int):
        num = str(num)
    
    if type == 'signed':
        sign = -1 if num[0] == '1' else 1
        start_idx = 1 if num[0] == '1' else 0
    else:
        sign = 1
        start_idx = 0
    
    s = 0
    for i in range(start_idx, len(num)):
        s += int(num[i]) * (2 ** (len(num) - i - 1))
    
    return sign * s

def signextend(digit, num, size=32):
    binary_num = bin(num & ((1 << size) - 1))[2:]
    return digit * (size - len(binary_num)) + binary_num

def decimaltobinary(num, type='unsigned', size=32):
    if type == 'signed':
        if num < 0:
            twoscomplement = (1 << size) + num
        else:
            twoscomplement = num
        return signextend('1' if num < 0 else '0', twoscomplement, size)
    
    if type == 'unsigned':
        if num < 0:
            raise OverflowError('Error: Illegal immediate overflow')
        return signextend('0', num, size)



class simulator:
    
    def __init__(self):
        self.output = open("C:\\Users\\kumar\\OneDrive\\Desktop\\output.txt", 'w+')
        self.zero = '00000000000000000000000000000000'
        self.ra = '00000000000000000000000000000000'
        self.sp = '00000000000000000000000100000000'
        self.gp = '00000000000000000000000000000000'
        self.tp = '00000000000000000000000000000000'
        self.t0 = '00000000000000000000000000000000'
        self.t1 = '00000000000000000000000000000000'
        self.t2 = '00000000000000000000000000000000'
        self.s0 = '00000000000000000000000000000000'
        self.s1 = '00000000000000000000000000000000'
        self.a0 = '00000000000000000000000000000000'
        self.a1 = '00000000000000000000000000000000'
        self.a2 = '00000000000000000000000000000000'
        self.a3 = '00000000000000000000000000000000'
        self.a4 = '00000000000000000000000000000000'
        self.a5 = '00000000000000000000000000000000'
        self.a6 = '00000000000000000000000000000000'
        self.a7 = '00000000000000000000000000000000'
        self.s2 = '00000000000000000000000000000000'
        self.s3 = '00000000000000000000000000000000'
        self.s4 = '00000000000000000000000000000000'
        self.s5 = '00000000000000000000000000000000'
        self.s6 = '00000000000000000000000000000000'
        self.s7 = '00000000000000000000000000000000'
        self.s8 = '00000000000000000000000000000000'
        self.s9 = '00000000000000000000000000000000'
        self.s10 ='00000000000000000000000000000000'
        self.s11 ='00000000000000000000000000000000'
        self.t3 = '00000000000000000000000000000000'
        self.t4 = '00000000000000000000000000000000'
        self.t5 = '00000000000000000000000000000000'
        self.t6 = '00000000000000000000000000000000'
        self.pc = 0
        self.registers = {
        '00000': 'zero',
        '00001': 'ra',
        '00010': 'sp',
        '00011': 'gp',
        '00100': 'tp',
        '00101': 't0',
        '00110': 't1',
        '00111': 't2',
        '01000': 's0',
        '01001': 's1',
        '01010': 'a0',
        '01011': 'a1',
        '01100': 'a2',
        '01101': 'a3',
        '01110': 'a4',
        '01111': 'a5',
        '10000': 'a6',
        '10001': 'a7',
        '10010': 's2',
        '10011': 's3',
        '10100': 's4',
        '10101': 's5',
        '10110': 's6',
        '10111': 's7',
        '11000': 's8',
        '11001': 's9',
        '11010': 's10',
        '11011': 's11',
        '11100': 't3',
        '11101': 't4',
        '11110': 't5',
        '11111': 't6'
        }
    def execution(self, line):
        if line[-7:] == '0110011' and line[17:20] == '000':
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
        pc_value = self.pc
        opcode = 'add'
        dest_reg = self.registers[line[20:25]]
        src_reg1 = self.registers[line[12:17]]
        src_reg2 = self.registers[line[7:12]]
        
        src1_value = binarytodecimal(self.registers[src_reg1], 'signed')
        src2_value = binarytodecimal(self.registers[src_reg2], 'signed')
        
        dest_value = decimaltobinary(src1_value + src2_value, 'signed')
        self.registers[dest_reg] = dest_value
        
        self.zero = '00000000000000000000000000000000'
        
        output_line = '0b'+decimaltobinary(pc_value, 'signed')+' 0b'+self.zero+' 0b'+self.ra+' 0b'+self.sp+' 0b'+self.gp+' 0b'+self.tp+' 0b'+self.t0+' 0b'+self.t1+' 0b'+self.t2+' 0b'+self.s0+' 0b'+self.s1+' 0b'+self.a0+' 0b'+self.a1+' 0b'+self.a2+' 0b'+self.a3+' 0b'+self.a4+' 0b'+self.a5+' 0b'+self.a6+' 0b'+self.a7+' 0b'+self.s2+' 0b'+self.s3+' 0b'+self.s4+' 0b'+self.s5+' 0b'+self.s6+' 0b'+self.s7+' 0b'+self.s8+' 0b'+self.s9+' 0b'+self.s10+' 0b'+self.s11+' 0b'+self.t3+' 0b'+self.t4+' 0b'+self.t5+' 0b'+self.t6+'\n'
        self.output.write(output_line)
        
        self.pc += 4
        
    def sub(self, line):
        print(globals()['pc'], 'sub')
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') - binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def sll(self, line):
        print(globals()['pc'], 'sll')
        imm = binarytodecimal(globals()[registers[line[7:12]]][-5:])
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') << binarytodecimal(imm), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4

    def slt(self, line):
        print(globals()['pc'], 'slt')
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') < binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()[registers[line[20:25]]] = decimaltobinary(1, 'signed')
            print(globals()[registers[line[20:25]]])
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def sltu(self, line):
        print(globals()['pc'], 'sltu')
        if binarytodecimal(globals()[registers[line[12:17]]]) < binarytodecimal(globals()[registers[line[7:12]]]):
            globals()[registers[line[20:25]]] = decimaltobinary(1, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def xor(self, line):
        print(globals()['pc'], 'xor')
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') ^ binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def srl(self, line):
        print(globals()['pc'], 'srl')
        imm = binarytodecimal(globals()[registers[line[7:12]]][-5:])
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') >> imm, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def OR(self, line):
        print(globals()['pc'], 'or')
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') | binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def AND(self, line):
        print(globals()['pc'], 'and')
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') & binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def lw(self, line):
        print(globals()['pc'], 'lw')
        globals()[registers[line[20:25]]] = memory[binarytodecimal(globals()[registers[line[12:17]]], 'signed') + binarytodecimal(line[:12], 'signed')]
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def addi(self, line):
        print(globals()['pc'], 'addi')
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') + binarytodecimal(line[:12], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def sltiu(self, line):
        print(globals()['pc'], 'sltiu')
        if binarytodecimal(globals()[registers[line[12:17]]]) < binarytodecimal(line[:12]):
            globals()[registers[line[20:25]]] = decimaltobinary(1, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def jalr(self, line):
        print(globals()['pc'], 'jalr')
        globals()[registers[line[20:25]]] = decimaltobinary(globals()['pc'] + 4, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        globals()['pc'] = (binarytodecimal(globals()[registers[line[12:17]]], 'signed') + binarytodecimal(line[:12], 'signed')) & ~1
        output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
                
    def sw(self, line):
        print(globals()['pc'], 'sw')
        print(binarytodecimal(globals()[registers[line[12:17]]], 'signed')+binarytodecimal(line[:7]+line[20:25], 'signed'))
        memory[binarytodecimal(globals()[registers[line[12:17]]], 'signed')+binarytodecimal(line[:7]+line[20:25], 'signed')] = globals()[registers[line[7:12]]]
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4 
    
    def beq(self, line):
        print(globals()['pc'], 'beq')
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') == binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
    
    def bne(self, line):
        globals()['zero'] = '00000000000000000000000000000000'
        print(globals()['pc'])
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') != binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            print(globals()['pc'], 'bne')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            print(globals()['pc'], 'bne', False)
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
            
    
    def blt(self, line):
        print(globals()['pc'], 'blt')
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') < binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4

    def bge(self, line):
        print(globals()['pc'], 'bge')
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]], 'signed') > binarytodecimal(globals()[registers[line[7:12]]], 'signed'):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
    
    def bltu(self, line):
        print(globals()['pc'], 'bltu')
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]]) < binarytodecimal(globals()[registers[line[7:12]]]):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
    
    def bgeu(self, line):
        print(globals()['pc'], 'bgeu')
        globals()['zero'] = '00000000000000000000000000000000'
        if binarytodecimal(globals()[registers[line[12:17]]]) > binarytodecimal(globals()[registers[line[7:12]]]):
            globals()['pc'] += binarytodecimal(line[0]+line[-8]+line[1:7]+line[-12:-8]+'0', 'signed')
            output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        else:
            output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
            globals()['pc'] += 4
            
    def auipc(self, line):
        print(globals()['pc'], 'auipc')
        globals()[registers[line[20:25]]] = decimaltobinary(globals()['pc'] + binarytodecimal(line[:20]+'000000000000', 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
        
    def lui(self, line):
        print(globals()['pc'], 'lui')
        globals()[registers[line[20:25]]] = line[:20]+'000000000000'
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        globals()['pc'] += 4
        
    def jal(self, line):
        print(globals()['pc'], 'jal')
        globals()[registers[line[20:25]]] = decimaltobinary(globals()['pc'] + 4, 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        globals()['pc'] += (binarytodecimal(line[0]+line[12:20]+line[11]+line[1:11]+'0', 'signed')) & ~1
        output.write('0b'+decimaltobinary(globals()['pc']-4, 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        
    def mul(self, line):
        globals()['pc'] += 4
        globals()[registers[line[20:25]]] = decimaltobinary(binarytodecimal(globals()[registers[line[12:17]]], 'signed') * binarytodecimal(globals()[registers[line[7:12]]], 'signed'), 'signed')
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
                
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
        globals()['pc'] += 4
        globals()[registers[line[20:25]]] = globals()[registers[line[12:17]]][::-1]
        globals()['zero'] = '00000000000000000000000000000000'
        output.write('0b'+decimaltobinary(globals()['pc'], 'signed')+' 0b'+globals()['zero']+' 0b'+globals()['ra']+' 0b'+globals()['sp']+' 0b'+globals()['gp']+' 0b'+globals()['tp']+' 0b'+globals()['t0']+' 0b'+globals()['t1']+' 0b'+globals()['t2']+' 0b'+globals()['s0']+' 0b'+globals()['s1']+' 0b'+globals()['a0']+' 0b'+globals()['a1']+' 0b'+globals()['a2']+' 0b'+globals()['a3']+' 0b'+globals()['a4']+' 0b'+globals()['a5']+' 0b'+globals()['a6']+' 0b'+globals()['a7']+' 0b'+globals()['s2']+' 0b'+globals()['s3']+' 0b'+globals()['s4']+' 0b'+globals()['s5']+' 0b'+globals()['s6']+' 0b'+globals()['s7']+' 0b'+globals()['s8']+' 0b'+globals()['s9']+' 0b'+globals()['s10']+' 0b'+globals()['s11']+' 0b'+globals()['t3']+' 0b'+globals()['t4']+' 0b'+globals()['t5']+' 0b'+globals()['t6']+'\n')
        
        
        
        
input_file = open("C:\\Users\\kumar\Downloads\\test1.txt", 'r')

l = input_file.readlines()

l = [i.strip('\n') for i in l]
print(l)

x = simulator()

while int(pc//4)-1 < len(l):
    if l[(pc//4)-1] == '00000000000000000000000001100011':
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
    
for i, j in enumerate(memory):
    output.write(str(i)+': '+memory[j]+'\n')


output.close()