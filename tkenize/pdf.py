import os

from pdfminer.high_level import extract_text

def pdf_tokenize(file_path, tkenizer):
    if os.path.isfile(file_path):
        pre_process(file_path)
    elif os.path.isdir(file_path):
        for file in os.scandir(file_path):
            pre_process(file, tkenizer)
    
def pre_process(file, tkenizer): 
    txt = extract_text(file)
    tokens = tkenizer(txt)