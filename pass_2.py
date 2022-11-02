from instructions import instructions

def object_code(df, sym_table):
    object_code_list = [' ']
    for i in range(1, df.index.stop):
        if df.Mnemonic[i] in instructions:
            if df.Mnemonic[i] == 'RSUB':
                object_code = "4C0000"
                
            elif type(instructions[df.Mnemonic[i]]) != list :
                op_code = bin(int(instructions[df.Mnemonic[i]], 16))[2: -1].rjust(7, '0')
                op_code += '1' if df.Value[i][0] == '#'  else  '0'
                
                op_code_index = op_code
                op_code_index += '1' if len(df.Value[i].split(',')) > 1 else  '0'
                
                if df.Value[i].split(',')[0] not in sym_table:
                    print('VARIABLE {0} DOES NOT EXIST'.format(df.Value[i].split(',')[0]))
                    quit()
                
                address = sym_table[df.Value[i].split(',')[0]]
                address_binary = bin(int(address, 16))[2: ].rjust(15, '0')
                object_code = op_code_index + address_binary
                
                object_code = hex(int(object_code, 2))[2: ].rjust(6, '0').upper()
                
        elif df.Mnemonic[i] == 'WORD':
            object_code = hex(int(df.Value[i]))[2: ].rjust(6, '0').upper()
        
        elif df.Mnemonic[i] == 'BYTE':
            if df.Value[i].split('\'')[0] == 'X':
                object_code = df.Value[i].split('\'')[1].upper()
            else:
                string = df.Value[i].split('\'')[1]
                object_code = ''
                for ascii_value in string.encode('ascii'):
                    object_code += str(ascii_value)
        else:
            object_code = ' '
        object_code_list.append(object_code)
        
    df.insert(4, 'Object_code', object_code_list)   
    return df

def pass_two(df, sym_table):
    df = object_code(df, sym_table)
    return