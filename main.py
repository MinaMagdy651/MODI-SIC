import utils
utils.make_directory()
program = utils.open_file('in.txt')
df = utils.return_df(program)
utils.return_intermediate(df)