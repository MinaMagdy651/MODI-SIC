from utils import make_directory
from pass_1 import pass_one
from pass_2 import pass_two
import time

make_directory()
path = input('Input file name: ')
pass_one_df, sym_table = pass_one(path)
pass_two(pass_one_df, sym_table)


