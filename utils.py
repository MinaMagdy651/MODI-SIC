import pandas as pd
from instructions import instructions
import re
import os
from pathlib import Path

# File handling, reemoving extra spaces and transforming to upper
def open_file(file):
    with open(file) as f:
        program = [re.sub(r'\s+', ' ', line).strip().upper() for line in f]
    return program

def prog_name(df):
    return df.iloc[0].Label.ljust(6, 'x')


# Parsing and returning the main data frame
def return_df(program):
    dict = []
    for line in program:
        
        # Removing the indeces and a part of the comment, no instruction will exceed 3 columns
        temp = line.split(" ")[1: 4]

        # Deleting comments
        if len(temp) < 1:
            continue
        if temp[0] == '.':
            continue

        # If the first column is an instruction then there is no label, so the 3rd coloumn is a comment
        if temp[0] in instructions:
            temp = temp[: 2] 
        
        # RSUB instruction and end no label
        if temp[0] == 'RSUB':
            label = ' '
            mnemonic = temp[0] 
            value = ' '
        # END INSTRUCTION
        elif temp[0]  == 'END':
            label = ' '
            mnemonic = temp[0]
            value = temp[1]

        # RSUB instruction with label
        elif temp[1] == 'RSUB':
            label = temp[0]
            mnemonic = temp[1]
            value = ' '

        # Fromat 1, 3 instruction without label
        elif temp[0] in instructions :
            label = ' '
            mnemonic = temp[0]
            value = temp[1]

        # Fromat 1, 3 instruction with label
        elif len(temp) >= 3:
            label = temp[0]
            mnemonic = temp[1]
            value = temp[2]
        
        # Appending a dictionary to the list of dictioneries
        dict.append({
            'Label':label,
            'Mnemonic': mnemonic,
            'Value': value
        })
    df = pd.DataFrame(dict)
    # Creating END directive if it doesn't exist
    if df.iloc[df.index.stop -1].Mnemonic != 'END':
        df2 = pd.DataFrame([[' ', 'END', ' ']], columns=df.columns)
        df = pd.concat([df, df2], ignore_index = True)
        print('NO END DIRECTIVE FOUND, CREATED ONE')
    print("DATA PARSING IS DONE")
    return df


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

# Makes the main direcory and handles if it exists already
def make_directory():
    folder_name = 'outputs'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return

# Crates a text file and write the symbol table inside of it
def return_symbol_table(list):
    fout = open("outputs/Symbol_Table.txt", "wt")
    for row in list:
        fout.write('{0}\t{1}\n'.format(row[0], row[1]))
    fout.close()
    print('SYMBOL TABLE FILE GENERATED')
    return