import pandas as pd
from instructions import instructions

# Adds Location Counter to the dataframe
def location_counter(df):
    start_index = df.Value[0]
    list_counter = [" ", start_index]
    counter = start_index

    for i in range(1, df.index.stop):

        if df.Mnemonic[i] in instructions:
            # Format 1 instruction
            if type(instructions[df.Mnemonic[i]]) == list:
                temp = hex(int(counter, 16) + 1)

            # Format 3 instruction
            else:
                temp = hex(int(counter, 16) + 3)
        
        if df.Mnemonic[i] == 'WORD':
            temp = hex(int(counter, 16) + 3)

        if df.Mnemonic[i] == 'BYTE':
            value = df.Value[i].split('\'')
            length = len(value[1])
            if value[0] == 'C':
                temp = hex(int(counter, 16) + int(length))
            else:
                temp = hex(int(counter, 16) + int(int(length)/2))

        # hex functions deals with integers ONLY
        # Counter is saved as a string hex value
        # int(counter, 16) transforms is to the integer value of the hex value
                
        # df.Value[i] is saved as a string decimal value
        # First, we transform it to integer using int(), then we add it in hex()
                
        if df.Mnemonic[i] == 'RESW':
            temp = hex(int(counter, 16) + int(df.Value[i]) *3)
            
        if df.Mnemonic[i] == 'RESB':
            temp = hex(int(counter, 16) + int(df.Value[i]))
            
            
        # Saving the new counter, and truncating the 0x at the beginning of the hex number
        counter = temp.split('x')[1].rjust(4, '0').upper()
        list_counter.append(counter)
    # Adding the location counter to the dataframe
    df.insert(0, 'Location_Counter', list_counter[:-1])
    return df

# Returns list with symbol table inside of it
def symbol_table(df):
    list = []
    # Ignoring the first row 
    for ind in range(1, df.index.stop):
        if df.Label[ind] != ' ':
            list.append([df.Location_Counter[ind], df.Label[ind]])
    return list
