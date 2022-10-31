import utils
import pass_1


utils.make_directory()
program = utils.open_file('in.txt')
df = utils.return_df(program)
utils.return_intermediate(df)
df = pass_1.location_counter(df)
print(df)