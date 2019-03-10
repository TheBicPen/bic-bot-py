import os

#helper functions
# def strip1(text: str, strip_text: str): #useless wtf
#     """
#     Returns a string with strip_text stripped from the beginning of text.
#     """
#     return text.lstrip(strip_text)

def strip2(text: str, strip_text: str):
    """
    Returns a string with everything up to and including the first occurence
    of strip_text and 1 additional character stripped from text. 
    If strip_text is not in text, return text[-1]
    """
    index = text.find(strip_text) + len(strip_text) + 1 # accounts for the space
    return text[index:]

def make_directory(dir):
    if not os.path.exists(dir) and dir != '':
        os.makedirs(dir)

def read_file(file:str) -> list:
    """
    Returns the contents of the file. If the file does not exist, creates the file
    and returns an empty list.
    #precondition: the directory exists
    """
    try:
        file_IO = open(file, "r", encoding="utf8")
        contents = file_IO.read().splitlines()
    except:
        dir = os.path.split(file)[0]
        make_directory(dir)
        file_IO = open(file, "x")
        contents = []
    finally:
        file_IO.close()
    return contents

def write_file(file:str, contents:str):
    read_file(file)
    file_IO = open(file, "w")
    file_IO.write(contents)
    file_IO.close


def read_dict_from_file(file:str, d={}):
    """
    Reads a file where each line has 2 words separated 
    by a space, and appends these words to dict as key-value
    pairs. 
    Precondition: each key is present in the file only once.
    """
    contents = read_file(file)
    for line in contents:
        num_semicolons = line.count(";")
        if num_semicolons == 0:
            print("line in file formatted improperly\n")
            return d
        elif num_semicolons == 1: #no semicolons in text
            words = line.split(";")
            d.update({words[0]: words[1]})
        else: # semicolons in text
            for ch_index in range(len(line)):
                if line[ch_index] == ";" and line[ch_index-1: ch_index] != "\\":
                    split_index = ch_index
            words = [line[:split_index], line[split_index + 1:]]
            words[0] = words[0].replace("\\", "")
            words[1] = words[1].replace("\\", "")
            d.update({words[0]: words[1]})
            
    return d

def write_dict_to_file(d:dict, fl:str):
    """
    Writes the key-value pairs in d as space-separated words
    in file. Each pair is on its own line.
    """
    file_obj = open(fl, "w+")
    for key, value in d.items():
        key = key.replace(";", "\\;")
        value = value.replace(";", "\\;")
        file_obj.write("{0};{1}\n".format(key, value))
    file_obj.close()

# def get_trans(fl:str, d:dict):
#     if d != {}:
