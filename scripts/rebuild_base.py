import pandas as pd

df = pd.read_excel('./data/base_2017_1.xlsx')
df1 = pd.read_excel('./data/base_2018_1.xlsx')
df2 = pd.read_excel('./data/base_2019_2.xlsx')
df_csv = pd.concat([df, df1, df2])
df_csv.to_csv('./data/base.csv', sep=',',index=False, encoding='utf-8')