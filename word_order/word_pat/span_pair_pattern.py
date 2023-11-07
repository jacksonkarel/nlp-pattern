from sentence_transformers import util

from all_minilm import ALL_MINILM
from word_order.word_pat.helpers import NOT_PAT_ENDS

class Span_pair_pattern:
    def __init__(self, long_pat, span_a_idx, tok_a, count_syn, span_b, synonyms):
        self.long_pat = long_pat,
        self.span_a_idx = span_a_idx,
        self.tok_a = tok_a,
        self.count_syn = count_syn,
        self.span_b = span_b,
        self.synonyms = synonyms

    def iter_span_b(self):
        print(self.tok_a)
        for tok_b in self.span_b:
            print(tok_b)
            if self.tok_a == tok_b and not (self.span_a_idx == 0 and self.tok_a in NOT_PAT_ENDS):
                self.long_pat.append(self.tok_a)
                return self.long_pat, self.synonyms

            elif self.synonyms:
                toks = [self.tok_a, tok_b]
                embeddings = []

                for toke in toks:
                    if toke in self.synonyms:
                        if tok_b in self.synonyms[toke]["synonyms"]:
                            return self.long_pat, self.synonyms
                        embed = self.synonyms[toke]["embeddings"]

                        
                    else:
                        #Compute embeddings 
                        embed = ALL_MINILM.encode(toke, convert_to_tensor=True)
                    
                    embeddings.append(embed)

                #Compute cosine-similarity
                cosine_scores = util.cos_sim(*embeddings)
                if cosine_scores[0][0] > .75:
                    # print(tok, tok_b)
                    if self.tok_a in self.synonyms:
                        self.check_synonyms(tok_b, self.tok_a)

                    elif tok_b in self.synonyms:
                        self.check_synonyms(tok_b, tok_b)
                    
                    else:
                        self.synonyms[self.tok_a]["synonyms"] = [tok_b]
                        self.synonyms[self.tok_b]["synonyms"] = [self.tok_a]
                        self.long_pat.append(self.tok_a)
                    
                    print(self.long_pat)
                    return self.long_pat, self.synonyms
        print(self.long_pat)
        return self.long_pat, self.synonyms
    
    def check_synonyms(self, tok_b, syn_check):
        toks = [self.tok_a, tok_b]
        for tok in toks:
            if tok != syn_check:
                to_check = tok
        if to_check not in self.synonyms[syn_check]["synonyms"]:
            self.synonyms[self.tok_a]["synonyms"].append(tok_b)
            self.synonyms[tok_b]["synonyms"].append(self.tok_a)
        
        self.long_pat.append(syn_check)
