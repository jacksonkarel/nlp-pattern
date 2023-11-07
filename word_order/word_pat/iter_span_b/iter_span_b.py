from sentence_transformers import util

from all_minilm import ALL_MINILM
from word_order.word_pat.helpers import NOT_PAT_ENDS

def iter_span_b(sc_data):
    tok = sc_data["token 1"]
    long_pat = sc_data["longest pattern"]
    synonyms = sc_data["synonyms"]
    for tok_b in sc_data["span 2"]:
        if tok == tok_b and not (sc_data["span 1 index"] == 0 and tok in NOT_PAT_ENDS):
            long_pat.append(tok)
            return long_pat, synonyms

        elif synonyms:
            toks = [tok, tok_b]
            embeddings = []

            for toke in toks:
                if toke in synonyms:
                    if tok_b in synonyms[toke]["synonyms"]:
                        return long_pat, synonyms
                    embed = synonyms[toke]["embeddings"]

                    
                else:
                    #Compute embeddings 
                    embed = ALL_MINILM.encode(toke, convert_to_tensor=True)
                
                embeddings.append(embed)

            #Compute cosine-similarity
            cosine_scores = util.cos_sim(*embeddings)
            if cosine_scores[0][0] > .75:
                # print(tok, tok_b)
                if tok in synonyms:
                    if tok_b not in synonyms[tok]["synonyms"]:
                        synonyms[tok]["synonyms"].append(tok_b)
                    
                    long_pat.append(tok)

                elif tok_b in synonyms:
                    if tok not in synonyms[tok_b]["synonyms"]:
                        synonyms[tok_b]["synonyms"].append(tok)
                    
                    long_pat.append(tok_b)
                
                else:
                    synonyms[tok]["synonyms"] = [tok_b]
                    long_pat.append(tok)
                
                return long_pat, synonyms

    return long_pat, synonyms