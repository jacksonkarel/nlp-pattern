import pickle
from itertools import chain, combinations

from tqdm import tqdm
import pandas as pd

def word_order(token_fn, output_fn, pat_sw=False):

    with open(token_fn, 'rb') as token_file:
        tokenized = pickle.load(token_file)
    
    counter = 0
    counter_b = 0
    with tqdm(total=len(tokenized)) as pbar:
        while tokenized and counter_b < 2:
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
                    # counter += 1
                else:
                    all_tp = pd.concat([all_tp, tp_df])
                    # print(all_tp)  
                counter_b += 1
            
            tokenized.pop(0)
            counter += 1
            pbar.update(1)
    
    print(all_tp)
        
            



    # with tqdm(total=len(tokenized)) as pbar:
    #     for tks in csv_gen:
    #         token_pattern(tks, next(tk_gen), pat_sw)
    #         pbar.update(1)

    # [token_pattern(tks, tokenized[idx +1], pat_sw) for idx, tks in tqdm(enumerate(tokenized))]
    
    # df = pd.DataFrame(pat_list)
    # pat_vc = df.value_counts()
    # pat_vc.to_csv(output_fn)