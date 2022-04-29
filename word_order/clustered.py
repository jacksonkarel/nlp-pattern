import json
import pickle

from segmenting.helpers import tokenize_clusters
from word_order.word_order import word_order

def clustered_word_order(input_fn, output_fn, pat_sw=False, count_syn=True, from_pickle=True, pickle_to=False):
    if from_pickle:
        with open(input_fn, 'rb') as token_file:
            tokenized = pickle.load(token_file)
    else:
        with open(input_fn) as json_file:
            clusters = json.load(json_file)
            
        tokenized = tokenize_clusters(clusters)

        if pickle_to:
            with open(pickle_to, 'ab') as token_file:
                pickle.dump(tokenized, token_file)
    
    word_order(tokenized, output_fn, pat_sw, count_syn)