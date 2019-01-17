#helper functions
def strip1(text: str, strip_text: str): #useless wtf
    """
    Returns a string with strip_text stripped from the beginning of text.
    """
    return text.lstrip(strip_text)

def strip2(text: str, strip_text: str):
    """
    Returns a string with everything up to and including the first occurence
    of strip_text and 1 additional character stripped from text. 
    If strip_text is not in text, return text[-1]
    """
    index = text.find(strip_text) + len(strip_text) + 1 # accounts for the space
    return text[index:]

#no params, simple text
def isbot(message):
    return "yes"

def ping(message):
    return "pong!"

#no params, other
def version():
    """
    Returns the version of the program, but python doesn't really have 
    program versions, unlike C#, so it just returns a placeholder string.
    """
    return "uh python doesn't really do that"

def settings(setting_to_val):
    """
    returns the value passed as an argument. Intended to be used to return the
    dict containing the settings.
    """
    return setting_to_val

#params: message only
def hello(message):
    return 'Hello {0.author.mention}'.format(message)

#params: command text only
def commit(commit_list:list):
    import random
    return commit_list[random.randrange(len(commit_list))]
	
def keeb(message, korean_list: list):
	for letter in message.content:
		if letter in korean_list:
			return True
	return False

#params: message and command text
def extrathicc(message, thicc_dict:dict):
    out = ""
    msg = strip2(message.content.upper(), "extrathicc")
    for ch in msg: #dict contains uppercase letters
        out += thicc_dict.get(ch, "")
    return out
#params: message and user data

def callme(message, user_to_nickname: dict): #not to be confused with discord nickname
    nickname = strip2(message.content, "callme") #command_text must be separate from the command by a space
    user_to_nickname.update({message.author: nickname})
    return "{0}, I will call you {1}".format(message.author.mention, nickname)

def myname(message): 
    pass
    get_name(message.author)
