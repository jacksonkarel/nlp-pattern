import re

import spacy

STOP_WORDS = ["a", "the", "it", "in", "this"]
SMALL_TOKENIZE = spacy.load("en_core_web_sm", exclude=["ner", "parser", "tagger", "lemmatizer"])

def txt_to_tokens(txt):
    doc = SMALL_TOKENIZE(txt)
    tokens = [t.text.lower() for t in doc if t.text.lower() not in STOP_WORDS and re.search("[a-zA-Z0-9]", t.text.lower())]
    return tokens

def extract_tokens(span):
    tokens = []
    for tok in span:
        clean_text = tok.text.strip().lower()
        if clean_text not in STOP_WORDS and re.search("[a-zA-Z0-9]", clean_text):
            tokens.append(clean_text)
    return tokens

def tokenize_clusters(clusters):
    all_tokenized = []
    for clust in clusters:
        tokenized = []
        texts = [txt for txt in clusters[clust]["texts"]]
        for doc in SMALL_TOKENIZE.pipe(texts):
            tokens = extract_tokens(doc)
            if tokens and tokens not in tokenized:
                tokenized.append(tokens)
    
        all_tokenized.append(tokenized)
    
    return all_tokenized