import pickle

from word_order import word_order

def unclustered_word_order(input_fn, output_fn, pat_sw=False, count_syn=True):
    with open(input_fn, 'rb') as token_file:
        all_tokenized = [pickle.load(token_file)]
    
    word_order(all_tokenized, output_fn, pat_sw, count_syn)