import pandas as pd
from instructions import instructions

def location_counter(df):
    start_index = df.Value[0]
    list_counter = [" ", start_index]
    counter = start_index

    for i in range(1, df.index.stop):
        if df.Mnemonic[i] in instructions:
            temp = hex(int(counter, 16) + 3)
            
        if df.Mnemonic[i] == 'WORD':
            temp = hex(int(counter, 16) + 3)
        if df.Mnemonic[i] == 'BYTE':
            value = df.Value[i].split('\'')
            length = len(value[1])
            if value == 'C':
                temp = hex(int(counter, 16) + int(length))
            else:
                temp = hex(int(counter, 16) + int(int(length)/2))
                
        if df.Mnemonic[i] == 'RESW':
            temp = hex(int(counter, 16) + int(hex(int(df.Value[i]) *3), 16))
            
        if df.Mnemonic[i] == 'RESB':
            temp = hex(int(counter, 16) + int(hex(int(df.Value[i])), 16))
            
    
        counter = temp.split('x')[1].rjust(4, '0').upper()
        list_counter.append(counter)
        
    df.insert(0, 'Location Counter', list_counter[:-1])
    return df