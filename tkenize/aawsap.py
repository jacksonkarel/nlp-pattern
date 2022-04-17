from tkenize.helpers import sm_doc, stop_words, stop_punct

def aawsap_tt(txt):
    doc = sm_doc(txt)
    s_punct_set = set(stop_punct)
    tokens = []
    for t in doc:
        strip_text = t.text.strip()
        if strip_text != "":
            lower_text = strip_text.lower()
            if lower_text not in stop_words:
                char_set = set(lower_text)
                if char_set.issubset(s_punct_set) is False:
                    tokens.append(lower_text)
    return tokens