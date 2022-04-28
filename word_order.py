import pickle
from itertools import chain, combinations
import json

from tqdm import tqdm
import pandas as pd
import spacy

from segmenting.helpers import extract_tokens

def clustered_word_order(input_fn, output_fn, pat_sw=False):
    with open(input_fn) as json_file:
        clusters = json.load(json_file)
    
    nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser", "tagger", "lemmatizer"])
    all_tokenized = []
    for clust in clusters:
        tokenized = []
        texts = [txt for txt in clusters[clust]["texts"]]
        for doc in nlp.pipe(texts):
            tokens = extract_tokens(doc)
            if tokens and tokens not in tokenized:
                tokenized.append(tokens)

        all_tokenized.append(tokenized)
    
    word_order(all_tokenized, output_fn, pat_sw)
    
def unclustered_word_order(input_fn, output_fn, pat_sw=False):
    with open(input_fn, 'rb') as token_file:
        all_tokenized = [pickle.load(token_file)]
    
    word_order(all_tokenized, output_fn, pat_sw)

def word_order(all_tokenized, output_fn, pat_sw=False):
    patterns = {}
    for clust in tqdm(all_tokenized):
        tok_comb = combinations(clust, 2)
        for tok_pair in tok_comb:
            long_pat = []
            for tok in tok_pair[0]:
                for tok_b in tok_pair[1]:
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