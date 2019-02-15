class Code:
    
    def __init__(self):
        self.dest_codes = ['', 'M', 'D', 'MD', 'A', 'AM', 'AD', 'AMD']
        self.comp_codes = {
        '0':'0101010', '1':'0111111', '-1':'0111010', 'D':'0001100',
        'A':'0110000', '!D':'0001101', '!A':'0110001', '-D':'0001111',
        '-A':'0110011', 'D+1':'0011111','A+1':'0110111','D-1':'0001110',
        'A-1':'0110010','D+A':'0000010','D-A':'0010011','A-D':'0000111',
        'D&A':'0000000','D|A':'0010101','':'xxxxxxx','M':'1110000','!M':'1110001',
        '-M':'1110011', 'M+1':'1110111','M-1':'1110010','D+M':'1000010','D-M':'1010011',
        'M-D':'1000111','D&M':'1000000', 'D|M':'1010101' 
        }
        self.jump_codes = ['', 'JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP']

    @staticmethod
    def bits(num):
        return bin(int(num))[2:]

    def dest(self, mnemonic):
        return self.bits(self.dest_codes.index(mnemonic)).zfill(3)

    def comp(self, mnemonic):
        return self.comp_codes[mnemonic]
    
    def jump(self, mnemonic):
        return self.bits(self.jump_codes.index(mnemonic)).zfill(3)

    def A(self, address):
        return '0' + self.bits(address).zfill(15)

    def C(self, comp, dest, jump):
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)

if __name__ == "__main__":
    c = Code()
    print(c.A("2"))
    print(c.C('D','D', ''))