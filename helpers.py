def txt_to_list(fname):
    with open(fname) as f:
        read_data = f.read()
    
    txt_list = read_data.split("\n")
    return txt_list
