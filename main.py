from utils import make_directory
from pass_1 import pass_one
from pass_2 import pass_two


make_directory()
pass_one_df, sym_table = pass_one()
pass_two(pass_one_df, sym_table)