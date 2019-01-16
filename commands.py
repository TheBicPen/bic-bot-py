#no params, simple text
def isbot(message):
    return "yes"

def ping(message):
    return "pong!"

#no params, other
def version():
    return "uh python doesn't really do that"

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
    index = message.content.find("extrathicc") + len("extrathicc")
    for ch in message.content.upper()[index:]: #dict contains uppercase letters
        out += thicc_dict.get(ch, "")
    return out
#params: message and user data
def callme(message, user_to_nickname):
    pass

def myname(message):
    pass
    get_name(message.author)
