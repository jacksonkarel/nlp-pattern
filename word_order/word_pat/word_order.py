from itertools import chain, combinations

from tqdm import tqdm
import pandas as pd

from word_order.word_pat.helpers import NOT_PAT_ENDS
from word_order.word_pat.span_pair_pattern import Span_pair_pattern

def word_order(all_tokenized, output_dir, count_syn=True, pat_sw=False):
    patterns = {}
    synonyms = {}
    for clust in tqdm(all_tokenized):
        span_comb = combinations(clust, 2)
        for span_pair in span_comb:
            long_pat = []
            for idx, tok in enumerate(span_pair[0]):
                spp = Span_pair_pattern(long_pat, idx, tok, count_syn, span_pair[1], synonyms)
                long_pat, synonyms = spp.iter_span_b()
                # print(long_pat)
                # if synonyms:
                #     print(synonyms)

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
    if count_syn:
        fname = "_syn"
    else:
        fname = ""
    output_fn = f"{output_dir}/patterns{fname}.csv"
    sorted_pat.to_csv(output_fn, index=False)

    if count_syn:
        syn_df = pd.DataFrame.from_dict(synonyms, orient='index')
        syn_fn = f"{output_dir}/synonyms.csv"
        syn_df.to_csv(syn_fn)