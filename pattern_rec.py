import pickle
from itertools import chain, combinations

from tqdm import tqdm

with open('tokenized.p', 'rb') as token_file:
    tokenized = pickle.load(token_file)

pattern_total = {}
for txt in tqdm(tokenized):
    for txt_b in tokenized:
        if txt != txt_b:
            long_pat = []
            for t in txt:
                for tb in txt_b:
                    if t == tb:
                        long_pat.append(t)
                        break

            powerset = chain.from_iterable(combinations(long_pat, r) for r in range(len(long_pat)+1))
            powerlist = list(powerset)
            for txt_pat in powerlist:
                if txt_pat not in pattern_total:
                    pattern_total[txt_pat] = 1
                else:
                    pattern_total[txt_pat] += 1

pat_list = pattern_total.items()