import os
import pickle
import fnmatch

from tqdm import tqdm

from pdfminer.high_level import extract_text

def pdf_t_pickle(file_path, segmenter, output):
    if os.path.isfile(file_path):
       texts = [extract_text(file_path)]
    elif os.path.isdir(file_path):
        texts = []
        file_count = len(fnmatch.filter(os.listdir(file_path), '*.*'))
        with tqdm(total=file_count) as pbar:
            for file in tqdm(os.scandir(file_path)):
                if file.path.endswith(".pdf"):
                    txt = extract_text(file.path)
                    texts.append(txt)
                
                pbar.update(1)

    if output.endswith(".p"):
        sents = segmenter(texts, txt=False)

        with open(output, 'wb') as sent_file:
            pickle.dump(sents, sent_file)
    
    else:
        sents = segmenter(texts)
        segmented = "\n".join(sents)
        
        with open(output, 'w') as f:
            f.write(segmented)