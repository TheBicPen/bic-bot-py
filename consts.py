# the current image classification source folder - useful for migrating between tensorflow v1 and v2
ML_lib = "image_classification_v2.image_classify_helpers"

# the command to run to retrieve the current IP address
IP_command = "wget -qO- https://ipecho.net/plain"

# the default settings for the bot
default_settings = {
    "command_str": "bb ",
    "annoyed_everyone": True,
    "everyone_string": "no u"
}

# a list of commands - this may be replaced with a mor dynamic solution in the future
cmd_list = "help, isbot, ping, version, settings, hello, commit, nut, extrathicc, \
        leet, keeb, callme, myname, call, name, deleteuser, defexplicit, defpattern, imagecat, tfstop, tfstart, \
        eval, exec, ip, modules"
