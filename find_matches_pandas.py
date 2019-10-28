# finds matches from two csv files, exports those matches to create new csv.
import pandas as pd

a = pd.read_csv('upload1.csv')
b = pd.read_csv('corr_length.csv')

c = pd.merge(a, b, how='inner', on=['fileURL'])

print(c)

c.to_csv('final_upload_list.csv')