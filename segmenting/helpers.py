import re

import spacy

stop_words = ["a", "the", "it", "in", "this"]

def txt_to_tokens(txt):
    doc = sm_doc(txt)
    tokens = [t.text.lower() for t in doc if t.text.lower() not in stop_words and re.search("[a-zA-Z0-9]", t.text.lower())]
    return tokens

def sm_doc(txt):
    nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser", "tagger", "lemmatizer"])
    doc = nlp(txt)
    return doc

def extract_tokens(span):
    tokens = []
    for tok in span:
        clean_text = tok.text.strip().lower()
        if clean_text not in stop_words and re.search("[a-zA-Z0-9]", clean_text):
            tokens.append(clean_text)
    return tokens