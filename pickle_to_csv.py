import pickle

import pandas as pd

with open("tokenizations/aawsap.p", 'rb') as token_file:
    tokenized = pickle.load(token_file)

df = pd.DataFrame(tokenized)
df.to_csv("tokenizations/aawsap.csv")