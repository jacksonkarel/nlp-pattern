import spacy

from segmenting.helpers import extract_tokens

def segment_sents(texts, txt=True):
    nlp = spacy.load("en_core_web_lg", exclude=["ner", "parser", "tagger", "lemmatizer"])
    nlp.enable_pipe("senter")
    sents = []
    for doc in nlp.pipe(texts):
        for sent in doc.sents:
            if txt:
                clean_sent = sent.text.strip()
                sents.append(clean_sent)
            else:
                tokens = extract_tokens(sent)
            
                if tokens:
                    sents.append(tokens)
    
    return sents
        
 