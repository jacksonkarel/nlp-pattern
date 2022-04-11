from pdfminer.high_level import extract_text

def pdf_tokenize(file):
    txt = extract_text(file)
    segments = txt.split('\n\n')
    segments.remove('')