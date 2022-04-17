import re

import spacy

from tkenize.helpers import stop_words

def aawsap_seg(texts):
    nlp = spacy.load("en_core_web_lg", exclude=["ner", "parser", "tagger", "lemmatizer"])
    nlp.enable_pipe("senter")
    sents = []
    for doc in nlp.pipe(texts):
        for sent in doc.sents:
            tokens = []
            for tok in sent:
                clean_text = tok.text.strip().lower()
                if clean_text not in stop_words and re.search("[a-zA-Z0-9]", clean_text):
                    tokens.append(clean_text)
            
            if tokens:
                sents.append(tokens)
    
    return sents
        
 