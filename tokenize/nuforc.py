import pickle

import pandas as pd

from tokenize.helpers import txt_to_tokens

def nuforc():
    df_text = pd.read_csv('data/nuforc.csv', usecols=[7])
    df_text.dropna()
    df_text['comments'] = df_text['comments'].astype(str)
    df_tokens = df_text["comments"].apply(txt_to_tokens)
    tokenized = df_tokens.to_list()
    tokenized.pop(0)
    with open('tokenized.p', 'ab') as token_file:
        pickle.dump(tokenized, token_file)