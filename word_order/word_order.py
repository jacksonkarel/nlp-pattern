from itertools import chain, combinations

from tqdm import tqdm
import pandas as pd
from sentence_transformers import util

from all_minilm import ALL_MINILM

NOT_PAT_ENDS = ["and", "or", "but", "though", "because"]

def iter_span_b(sc_data):
    tok = sc_data["token 1"]
    long_pat = sc_data["longest pattern"]
    for tok_b in sc_data["span 2"]:
        if tok == tok_b and not (sc_data["span 1 index"] == 0 and tok in NOT_PAT_ENDS):
            long_pat.append(tok)
            return long_pat

        elif sc_data["count synonyms"]:
            #Compute embeddings for both words
            embeddings1 = ALL_MINILM.encode(tok, convert_to_tensor=True)
            embeddings2 = ALL_MINILM.encode(tok_b, convert_to_tensor=True)

            #Compute cosine-similarity
            cosine_scores = util.cos_sim(embeddings1, embeddings2)
            synonyms = sc_data["synonyms"]
            if cosine_scores[0][0] > .75:
                if tok in synonyms:
                    if tok_b not in synonyms[tok]:
                        synonyms[tok].append(tok_b)
                    
                    long_pat.append(tok)

                elif tok_b in synonyms:
                    if tok not in synonyms[tok_b]:
                        synonyms[tok_b].append(tok)
                    
                    long_pat.append(tok_b)
                
                else:
                    synonyms[tok] = [tok_b]
                    long_pat.append(tok)
                
                return long_pat

    return long_pat

def word_order(all_tokenized, output_fn, count_syn=True, pat_sw=False):
    patterns = {}
    synonyms = {}
    for clust in tqdm(all_tokenized):
        span_comb = combinations(clust, 2)
        for span_pair in span_comb:
            long_pat = []
            for idx, tok in enumerate(span_pair[0]):
                sc_data = {
                    "longest pattern": long_pat,
                    "span 1 index": idx,
                    "token 1": tok,
                    "count synonyms": count_syn,
                    "span 2": span_pair[1],
                    "synonyms": synonyms
                }
                long_pat = iter_span_b(sc_data)

            if long_pat:
                if long_pat[-1] in NOT_PAT_ENDS:
                    long_pat.pop()
                
                if pat_sw:
                    long_pat = long_pat - pat_sw

                powerset = chain.from_iterable(combinations(long_pat, r) for r in range(len(long_pat)+1))
                for pat in powerset:
                    if pat:
                        pat_set = set(pat)
                        stop_comb = {"and", "or", "but", "though", "if", "were", "he", "she", "not", "his", "her", "because", "they"
                        "they", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "so", "when", "how", "which", "where", "who", 
                        "whom", "therefore"}
                        if not pat_set.issubset(stop_comb):
                            pat_str = " ".join(pat)
                            if pat_str in patterns:
                                patterns[pat_str] += 1
                            else:
                                patterns[pat_str] = 1
            
                
    pat_df = pd.DataFrame()
    pat_df['pattern'] = patterns.keys()
    pat_df['count'] = patterns.values()
    pat_df['sentLenByCount'] = pat_df['pattern'].apply(len) * pat_df['count']
    sorted_pat = pat_df.sort_values(['sentLenByCount'], ascending=False)
    sorted_pat.to_csv(output_fn, index=False)

    if count_syn:
        syn_df = pd.DataFrame.from_dict(synonyms, orient='index')
        syn_df.to_csv("synonyms.csv")