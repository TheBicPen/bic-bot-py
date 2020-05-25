import collections
from discord.embeds import Embed

class MessageResponse:
    message="" # messages longer than 2k chars may be split before being sent
    debug="" # may be printed to stdout, stderr, a log file, or posted to discord
    files=[]
    embed=None
    delete_after=None
    tts=False
    def __init__(self, message = "", debug = "", files=None, embed=None, delete_after=None, tts=False):
        self.message = message
        self.debug = debug
        if isinstance(files, collections.Iterable):
            self.files.extend(files)
        if isinstance(embed, Embed):
            self.embed = embed
        if delete_after is not None and delete_after > 0:
            self.delete_after = delete_after
        self.tts=tts

