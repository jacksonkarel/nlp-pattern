import pickle
from itertools import chain, combinations

from tqdm import tqdm
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi


with open('tokenized.p', 'rb') as token_file:
    tokenized = pickle.load(token_file)

pattern_total = {}
for txt in tqdm(tokenized):
    for txt_b in tqdm(tokenized):
        if txt != txt_b:
            long_pat = []
            for t in txt:
                for tb in txt_b:
                    if t == tb:
                        long_pat.append(t)
                        break
            long_pat_len = len(long_pat)
            long_pat_set = set(long_pat)
            pat_stop_words = {"it", "in", "around", "this", "after", "/"}
            difference = long_pat_set - pat_stop_words
            if len(difference) > 0:
                powerset = chain.from_iterable(combinations(long_pat, r) for r in range(len(long_pat)+1))
                powerlist = list(powerset)
                powerlist.pop(0)
                
                for txt_pat in powerlist:
                    if txt_pat not in pattern_total:
                        pattern_total[txt_pat] = 1
                    else:
                        pattern_total[txt_pat] += 1

pat_list = pattern_total.items()
df = pd.DataFrame(pat_list)
df.to_csv('patterns/patterns.csv')

kaggle = KaggleApi()
kaggle.authenticate()
kaggle.dataset_create_version("patterns", "Generated from nlp-pattern script", convert_to_csv=False, delete_old_versions=True)