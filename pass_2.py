from instructions import instructions
from utils import out_pass2, prog_name, hte_record_out


# Returns the object code 
def object_code(df, sym_table):
    object_code_list = [' ']
    # First line has no object code, so we are ignoring it
    for i in range(1, df.index.stop):
        if df.Mnemonic[i] in instructions:
            # RSUB instruction
            if df.Mnemonic[i] == 'RSUB':
                object_code = "4C0000"
            
            # Format 3
            elif type(instructions[df.Mnemonic[i]]) != list:
                # Getting the hex value of the instruction then transfering it to binary and removing the 0b indicator
                # Then filling it in 7 bytes
                op_code = bin(int(instructions[df.Mnemonic[i]], 16))[2: -1].rjust(7, '0')

                # Checking the immidiate value
                op_code += '1' if df.Value[i][0] == '#'  else  '0'

                # Checking for indirect accesing, 'BUFFER, X'
                op_code_index = op_code
                op_code_index += '1' if len(df.Value[i].split(',')) > 1 else  '0'

                # Format 3, immidiate 
                if df.Value[i][0] == '#':
                    immidiate = bin(int(df.Value[i].split('#')[1], 16))[2: ].rjust(15, '0')
                    object_code = op_code_index + immidiate

                # Format 3, normal    
                elif df.Value[i][0] != '#':
                    address = sym_table[df.Value[i].split(',')[0]]
                    address_binary = bin(int(address, 16))[2: ].rjust(15, '0')
                    object_code = op_code_index + address_binary
                    
                # Making sure the value exists in the symbol table
                elif df.Value[i].split(',')[0] not in sym_table:
                    print('VARIABLE {0} DOES NOT EXIST'.format(df.Value[i].split(',')[0]))
                    quit()
                 # Trasforming the object code from binary to decimal and fitting it in 6 digits
                object_code = hex(int(object_code, 2))[2: ].rjust(6, '0').upper()

            # Format 1     
            else:
                object_code = instructions[df.Mnemonic[i]][0]

        elif df.Mnemonic[i] == 'WORD':
            object_code = hex(int(df.Value[i]))[2: ].rjust(6, '0').upper()
        
        elif df.Mnemonic[i] == 'BYTE':
            if df.Value[i].split('\'')[0] == 'X':
                object_code = df.Value[i].split('\'')[1].upper()
            else:
                string = df.Value[i].split('\'')[1]
                # From ascii to hex
                object_code = string.encode('utf-8').hex().upper()
        # Directives           
        else:
            object_code = ' '
        object_code_list.append(object_code)
        
    df.insert(4, 'Object_code', object_code_list)   
    return df

# A helper function that calculated how many bytes each line has taken
def byte_counter(df):
    byte_list = ['0']
    for i in range(1, df.index.stop):
        if df.Mnemonic[i] == 'WORD':
            byte_count = '3'
            
        elif df.Mnemonic[i] == 'BYTE':
            if df.Value[i].split('\'')[0] == 'X':
                byte_count = int(len(df.Value[i].split('\'')[1])/2)
            else:
                byte_count = len(df.Value[i].split('\'')[1])
                
        elif df.Mnemonic[i] in instructions:
            # Instruction 1 format
            if type(df.Mnemonic[i]) == list:
                byte_count = '1'

            # Instruction 3 format
            else:
                byte_count = '3'
        else:
            byte_count = '0'
        byte_list.append(byte_count)
    df.insert(5, 'Bytes', byte_list) 
    return df

# Return the head string
def head(df):
    program_name = prog_name(df)
    # Location of first executable instruction
    start = df.iloc[1].Location_Counter.rjust(6, '0')

    # Location of last executable instruction
    end = df.iloc[df.index.stop -1].Location_Counter.rjust(6, '0')

    length = hex(int(end, 16) - int(start, 16))[2: ].rjust(6, '0').upper()
    return 'H'+program_name+start+length

# Return the end string
def end(df):
    start = df.iloc[1].Location_Counter.rjust(6, '0')
    return 'E'+start


def text_helper(start, df):
    address = df.iloc[start].Location_Counter.rjust(6, '0')
    counter = 0
    index = start
    # Couting the numbers of bytes, not to exceed the limit which is 1E
    while(counter + int(df.iloc[index].Bytes) <= 30):
        # RESB or RESW
        if df.iloc[index].Bytes == '0':
            break
            
        counter += int(df.iloc[index].Bytes)
        index += 1
        
    end = df.iloc[index].Location_Counter
    length = hex(int(end, 16) - int(address, 16))[2: ].rjust(2, '0').upper()
    
    object_codes = ''
    for i in range(start, index):
        object_codes += df.iloc[i].Object_code

    return 'T' + address + length + object_codes, index

# Returns a list of text fields
def text_generator(df):
    texts = []
    i = 0
    while(i < df.index.stop):
        if df.iloc[i].Bytes == '0':
            i += 1
        else:
            text, i = text_helper(i, df)
            texts.append(text)
    return texts
# Returns the HTE record
def hte_record(df):
    hte = []
    hte.append(head(df))
    texts = text_generator(df)
    for text in texts:
        hte.append(text)
    hte.append(end(df))
    return hte

def pass_two(df, sym_table):
    print('-' * 30)
    print('*' *5 + ' PASS TWO STARTED' + '*' *5)
    df = object_code(df, sym_table)
    print("OBJECT CODE GENERATED")
    out_pass2(df)
    df = byte_counter(df)
    
    hte = hte_record(df)
    hte_record_out(hte)

    print('*' *5 + ' PASS TWO ENDED ' + '*' *5)
    print('-' * 30)
    return