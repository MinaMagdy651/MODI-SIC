import pandas as pd
from instructions import instructions
import re
import os
from pathlib import Path

def open_file(file):
    with open(file) as f:
        program = [re.sub(r'\s+', ' ', line).strip().upper() for line in f]
    return program

def prog_name(df):
    return df.iloc[0].Label.ljust(6, 'x')

def return_df(program):

    dict = []
    for line in program:
        
        temp = line.split(" ")[1: 4]
        
        if temp[0] == '.':
            continue
            
        if temp[0] in instructions:
            temp = temp[: 2] 
        
        if temp[0] in instructions and (type(instructions[temp[0]]) == list or temp[0] == 'RSUB'):
            label = ' '
            mnemonic = temp[0]
            value = ' '

        elif temp[1] in instructions and (type(instructions[temp[1]]) == list or temp[1] == 'RSUB'):
            label = temp[0]
            mnemonic = temp[1]
            value = ' '
            
        elif temp[0] in instructions:
            label = ' '
            mnemonic = temp[0]
            value = temp[1]

        elif len(temp) >= 3:
            label = temp[0]
            mnemonic = temp[1]
            value = temp[2]
        

        dict.append({
            'Label':label,
            'Mnemonic': mnemonic,
            'Value': value
        })

    df = pd.DataFrame(dict)
    return df

def return_intermediate(df):
    fout = open("outputs/intermediate.txt", "wt")
    for ind in df.index:
        if(df.Label[ind] == ' '):
            fout.write('\t\t{0}\t{1}\n'.format(df.Mnemonic[ind].ljust(8, ' '), df.Value[ind]).ljust(8, ' '))
        
        else:
            fout.write('{0}\t{1}\t{2}\n'.format(df.Label[ind].ljust(8, ' '), df.Mnemonic[ind].ljust(8, ' '), df.Value[ind].ljust(8, ' ')))
            
    fout.close()
    return

def make_directory():
    folder_name = 'outputs'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return

