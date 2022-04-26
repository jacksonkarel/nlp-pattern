import pickle
from itertools import chain, combinations

from tqdm import tqdm
import pandas as pd

def word_order(token_fn, output_fn, pat_sw=False):

    with open(token_fn, 'rb') as token_file:
        tokenized = pickle.load(token_file)
    
    counter = 0

    with tqdm(total=len(tokenized)) as pbar:
        while tokenized:
            top_pats = {}
            tks = tokenized[0]
            for tks_b in tqdm(tokenized[1:]):
                long_pat = []
                for tok in tks:
                    for tok_b in tks_b:
                        if tok == tok_b:
                            long_pat.append(tok)
                            break
                
                if pat_sw:
                    long_pat = long_pat - pat_sw
                if long_pat:
                    powerset = chain.from_iterable(combinations(long_pat, r) for r in range(len(long_pat)+1))
                    for pat in powerset:
                        if pat:
                            pat_set = set(pat)
                            stop_comb = {"and", "or", "but", "though", "if", "were", "he", "she", "not", "his", "her", "because", "they"
                            "they", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "so", "when", "how", "which", "where", "who", 
                            "whom", "therefore"}
                            if not pat_set.issubset(stop_comb):
                                pat_str = " ".join(pat)
                                if counter > 0:
                                    if not all_tp['pattern'].str.contains(pat_str).any():
                                        if pat_str in top_pats:
                                            top_pats[pat_str] += 1
                                        else:
                                            top_pats[pat_str] = 1
                                else:
                                    if pat_str in top_pats:
                                        top_pats[pat_str] += 1
                                    else:
                                        top_pats[pat_str] = 1
            
            if top_pats:
                tp_df = pd.DataFrame()
                tp_df['pattern'] = top_pats.keys()
                tp_df['count'] = top_pats.values()
                tp_df['sentLenByCount'] = tp_df['pattern'].apply(len) * tp_df['count']
                if counter < 1:
                    all_tp = tp_df
                else:
                    all_tp = pd.concat([all_tp, tp_df])
            
            tokenized.pop(0)
            if counter < 1:
                counter += 1
            pbar.update(1)
        
    all_tp.to_csv(output_fn)