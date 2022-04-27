import re

import spacy

from segmenting.helpers import stop_words

def aawsap_seg(texts, txt=True):
    nlp = spacy.load("en_core_web_lg", exclude=["ner", "parser", "tagger", "lemmatizer"])
    nlp.enable_pipe("senter")
    sents = []
    for doc in nlp.pipe(texts):
        for sent in doc.sents:
            if txt:
                clean_sent = sent.text.strip()
                sents.append(clean_sent)
            else:
                tokens = []
                for tok in sent:
                    clean_text = tok.text.strip().lower()
                    if clean_text not in stop_words and re.search("[a-zA-Z0-9]", clean_text):
                        tokens.append(clean_text)
            
                if tokens:
                    sents.append(tokens)
    
    return sents
        
 