import spacy

stop_words = [".", "?", "!", "-", " ", ",", ";", ":", "a", "the", "(", ")"]

def txt_to_tokens(txt):
    nlp = spacy.load("en_core_web_sm", exclude=["ner", "parser", "tagger", "lemmatizer"])
    doc = nlp(txt)
    tokens = [t.text.lower() for t in doc if t.text.lower() not in stop_words]
    return tokens