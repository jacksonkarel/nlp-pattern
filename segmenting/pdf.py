import os
import pickle
import fnmatch

from tqdm import tqdm
from pdfminer.high_level import extract_text

from helpers import txt_to_list


def segment_file(file_path, segmenter, output):
    pdf_end = ".pdf"
    txt_end = ".txt"
    if os.path.isfile(file_path):
        if file_path.path.endswith(pdf_end):
           texts = [extract_text(file_path)]
        elif file_path.path.endswith(txt_end):
            texts = txt_to_list(file_path)

    elif os.path.isdir(file_path):
        texts = []
        file_count = len(fnmatch.filter(os.listdir(file_path), '*.*'))
        with tqdm(total=file_count) as pbar:
            for file in tqdm(os.scandir(file_path)):
                if file.path.endswith(pdf_end):
                    txt = extract_text(file.path)
                    texts.append(txt)
                elif file.path.endswith(txt_end):
                    txt = txt_to_list(file)
                    texts.append(txt)
                
                pbar.update(1)

    if output.endswith(".pickle"):
        sents = segmenter(texts, txt=False)

        with open(output, 'wb') as sent_file:
            pickle.dump(sents, sent_file)
    
    else:
        sents = segmenter(texts)
        segmented = "\n".join(sents)
        
        with open(output, 'w') as f:
            f.write(segmented)