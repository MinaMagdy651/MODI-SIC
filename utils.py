import pandas as pd
from instructions import instructions, directives
import re
import os
from pathlib import Path

# File handling, reemoving extra spaces and transforming to upper
def open_file(file):
    with open(file) as f:
        program = [re.sub(r'\s+', ' ', line).strip().upper() for line in f]
    return program

# Return program name
def prog_name(df):
    return df.iloc[0].Label.ljust(6, 'x')

# Parsing and returning the main data frame
def return_df(program):
    dict = []
    for line in program:
        line = line.split(" ")[1: 4]
        # Removing comments and empty lines
        if len(line) < 1 or line[0] == '.':
            continue
            
        # If the first one is an instruction, then there is no label
        if line[0] in instructions or line[0] == 'END':
            line = line[: 2]
            
        # RSUB without label
        if line[0] == 'RSUB':
            label = ' '
            mnemonic = line[0]
            value = ' '
            
        
        # RSUB with label
        elif len(line) >= 2 and line[1] == 'RSUB':
            label = line[0]
            mnemonic = line[1]
            value = ' '
            
         # End Directive
        elif line[0] == 'END':
            label = ' '
            mnemonic = line[0]
            value = line[1]
        
        # No label
        elif line[0] in instructions:
            # Format 1 no label
            if type(instructions[line[0]]) == list:
                label = ' '
                mnemonic = line[0]
                value = ' '

            # Format 3 no label
            else:
                label = ' '
                mnemonic = line[0]
                value = line[1]
                        
        # Format 1 with label
        elif len(line) >= 2 and line[1] in instructions and type(instructions[line[1]]) == list:
                label = line[0]
                mnemonic = line[1]
                value = ' '
        # Format 3 with label and directives
        else:
            label = line[0]
            mnemonic = line[1]
            value = line[2]
            
        dict.append({
            'Label':label,
            'Mnemonic': mnemonic,
            'Value': value
        })
    df = pd.DataFrame(dict)
    # Creating END directive if it doesn't exist
    if df.iloc[df.index.stop -1].Mnemonic != 'END':
        df2 = pd.DataFrame([[' ', 'END', df.iloc[0].Value]], columns=df.columns)
        df = pd.concat([df, df2], ignore_index = True)
    return df


# Makes the main direcory and handles if it exists already
def make_directory():
    folder_name = 'outputs'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return


# Creates a text file and writes the dataframe inside of it
def return_intermediate(df):
    fout = open("outputs/intermediate.txt", "wt")
    for ind in df.index:
        if(df.Label[ind] == ' '):
            fout.write('\t\t{0}\t{1}\n'.format(df.Mnemonic[ind].ljust(8, ' '), df.Value[ind]).ljust(8, ' '))
        
        else:
            fout.write('{0}\t{1}\t{2}\n'.format(df.Label[ind].ljust(8, ' '), df.Mnemonic[ind].ljust(8, ' '), df.Value[ind].ljust(8, ' ')))
            
    fout.close()
    print('INTERMEDIATE FILE GENERATED')
    return

# Crates a text file and write the full program inside of it
def out_pass1(df):
    fout = open("outputs/out_pass1.txt", "wt")
    for ind in df.index:
        fout.write('{0}\t{1}\t{2}\t{3}\n'.format(df.Location_Counter[ind].ljust(8, ' '), df.Label[ind].ljust(8, ' '), df.Mnemonic[ind].ljust(8, ' '), df.Value[ind]).ljust(8, ' '))
    fout.close()
    print('OUT PASS ONE FILE GENERATED')
    return

# Crates a text file and write the symbol table inside of it
def return_symbol_table(list):
    fout = open("outputs/symTable.txt", "wt")
    for key, value in list.items():
        fout.write('{0}\t{1}\n'.format(key.ljust(8, ' '), value))

    fout.close()
    print('SYMBOL TABLE FILE GENERATED')
    return

# Crates a text file and write the full program inside of it
def out_pass2(df):
    fout = open("outputs/out_pass2.txt", "wt")
    for ind in df.index:
        fout.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.format(df.Location_Counter[ind].ljust(8, ' '), df.Label[ind].ljust(8, ' '), df.Mnemonic[ind].ljust(8, ' '), df.Value[ind].ljust(8, ' '), df.Object_code[ind]))
    fout.close()
    print('OUT PASS TWO FILE GENERATED')
    return

def hte_record_out(list):
    fout = open("outputs/HTE.txt", "wt")
    for item in list:
        fout.write(item + '\n')
    fout.close()
    print('HTE RECORD FILE GENERATED')
    return