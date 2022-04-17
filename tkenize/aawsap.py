import spacy
from tqdm import tqdm

from tkenize.helpers import stop_words, stop_punct

def aawsap_seg(texts):
    nlp = spacy.load("en_core_web_lg", exclude=["ner", "parser", "tagger", "lemmatizer"])
    nlp.enable_pipe("senter")
    sents = []
    texts_len = len(texts)
    s_punct_set = set(stop_punct)
    with tqdm(total=texts_len) as pbar:
        for doc in nlp.pipe(texts):
            for sent in doc.sents:
                tokens = []
                for tok in sent:
                    strip_text = tok.text.strip()
                    if strip_text != "":
                        lower_text = strip_text.lower()
                        if lower_text not in stop_words:
                            char_set = set(lower_text)
                            if char_set.issubset(s_punct_set) is False:
                                tokens.append(lower_text)
                
                sents.append(tokens)
        
        pbar.update(1)
    
    return sents
        
 