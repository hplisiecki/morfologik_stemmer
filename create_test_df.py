import pandas as pd

sentence = 'Poszedłem do sklepu żeby kupić trochę mleka.'
df = pd.DataFrame()
df['sentence'] = [sentence] * 1000
# save
df.to_csv('data/test_df.csv', index = False)

# load
df = pd.read_csv('data/test_df.csv')