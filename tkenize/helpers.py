import spacy

stop_words = [".", "?", "!", "-", " ", ",", ";", ":", "a", "the", "(", ")", "it", "in", "this", "/", "\n", "\n\n"]

def txt_to_tokens(txt):
    doc = sm_doc(txt)
    tokens = [t.text.lower() for t in doc if t.text.lower() not in stop_words]
    return tokens

def sm_doc(txt):
    nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser", "tagger", "lemmatizer"])
    doc = nlp(txt)
    return doc