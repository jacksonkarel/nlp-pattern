import pickle
import os

import pandas as pd

from segmenting.helpers import txt_to_tokens

def segment_nuforc(txt=True):
    df_text = pd.read_csv('data/nuforc.csv', usecols=[7])
    df_text.dropna()
    df_text['comments'] = df_text['comments'].astype(str)
    df_text['comments'] = df_text['comments'].str.strip()
    if txt:
        os.makedirs("sentences", exist_ok=True)
        df_text.to_csv("sentences/nuforc.txt", header=None, index=None)
    else:
        df_tokens = df_text["comments"].apply(txt_to_tokens)
        tokenized = df_tokens.to_list()
        tokenized.pop(0)
        os.makedirs("tokenizations", exist_ok=True)
        with open('tokenizations/nuforc.p', 'ab') as token_file:
            pickle.dump(tokenized, token_file)