import pickle

def patterns(tok_a_fn, tok_b_fn):
    with open(tok_a_fn, 'rb') as embed_file:
        tok_a = pickle.load(embed_file)
    with open(tok_b_fn, 'rb') as embed_file:
        tok_b = pickle.load(embed_file)
    

    