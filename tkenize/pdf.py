import os
import pickle
import fnmatch

from tqdm import tqdm

from pdfminer.high_level import extract_text

def pdf_t_pickle(file_path, tkenizer, pickle_fn):
    if os.path.isfile(file_path):
        all_pdf_tks = pdf_tokenize(file_path, tkenizer)
    elif os.path.isdir(file_path):
        all_pdf_tks = []
        file_count = len(fnmatch.filter(os.listdir(file_path), '*.*'))
        with tqdm(total=file_count) as pbar:
            for file in tqdm(os.scandir(file_path)):
                if file.path.endswith(".pdf"):
                    pdf_tokens = pdf_tokenize(file.path, tkenizer)
                    all_pdf_tks.append(pdf_tokens)
                
                pbar.update(1)
                
    print(all_pdf_tks)
    with open(pickle_fn, 'ab') as token_file:
        pickle.dump(all_pdf_tks, token_file)

def pdf_tokenize(file, tkenizer): 
    txt = extract_text(file)
    tokens = tkenizer(txt)
    return tokens