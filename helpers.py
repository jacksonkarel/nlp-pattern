def txt_to_list(fname):
    with open(fname) as f:
        read_data = f.read()
    
    txt_list = read_data.split("\n")
    tl_clean = [txt for txt in txt_list if txt]
    return tl_clean
