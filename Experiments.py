import pandas as pd
# 0 - timeframe
# 18 - Digi
# 21 - Antena3
df_3 = pd.read_excel('Audiente Sferturi/Digi 24-audiente zilnice 2023-02-02.xlsx', sheet_name=1)
df_4 = pd.read_excel('Audiente Sferturi/Digi 24-audiente zilnice 2023-02-03.xlsx', sheet_name=1)
print(df_3.iloc[1:109, [0, 18, 21]])
print(df_4.iloc[1:109, [0, 18, 20]])

if df_3.iloc[1, 21] == "Antena 3 CNN":
    print("yes!")



#print(df.iloc[1:109, [0, 18, 20]])
#
# csv_file = df.to_csv('Test.csv')
# csv_file_without_header = df.to_csv('Test_no_header.csv', header=False)
#
# csv = pd.read_csv('Test_no_header.csv')


