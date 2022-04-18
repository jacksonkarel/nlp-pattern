import pickle
from itertools import chain, combinations

from tqdm import tqdm
import pandas as pd

def word_order(token_fn, output_fn, pat_sw=False):
    with open(token_fn, 'rb') as token_file:
        tokenized = pickle.load(token_file)

    pat_list = []
    with tqdm(total=len(tokenized)) as pbar:
        while tokenized:
            txt = tokenized[0]
            for txt_b in tokenized[1:]:
                long_pat = []
                for t in txt:
                    for tb in txt_b:
                        if t == tb:
                            long_pat.append(t)
                            break
                long_pat_set = set(long_pat)
                if pat_sw:
                    long_pat_set = long_pat_set - pat_sw
                if long_pat_set:
                    powerset = chain.from_iterable(combinations(long_pat, r) for r in range(len(long_pat)+1))
                    pat_list += powerset
            
            tokenized.pop(0)
            pbar.update(1)

    df = pd.DataFrame(pat_list)
    pat_vc = df.value_counts()
    pat_vc.to_csv(output_fn)