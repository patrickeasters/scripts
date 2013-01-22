# Copyright (C) 2010  Kevin Morris <kevr@exdevelopment.net>
# lnotify made to use for libnotify notifications
# must have /usr/bin/send-notify
# This script was adapted from 'notify'
# Hope you guys like it :O
#
# 0.1.2
# added option to display weechat's icon by tomboy64

import weechat, string, subprocess, os

weechat.register("lnotify", "kevr", "0.1.2", "GPL3", "lnotify - A libnotify script for weechat", "", "")

# Set up here, go no further!
settings = {
    "show_highlight"     : "on",
    "show_priv_msg"      : "on",
    "icon"		 : "/usr/share/icons/hicolor/32x32/apps/weechat.png"
}

# Init everything
for option, default_value in settings.items():
    if weechat.config_get_plugin(option) == "":
        weechat.config_set_plugin(option, default_value)

# Hook privmsg/hilights
weechat.hook_print("", "irc_privmsg", "", 1, "get_notified", "")

# Functions
def get_notified(data, bufferp, uber_empty, tagsn, isdisplayed,
        ishilight, prefix, message):

    if (weechat.buffer_get_string(bufferp, "localvar_type") == "private" and
            weechat.config_get_plugin('show_priv_msg') == "on"):
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                weechat.buffer_get_string(bufferp, "name"))
        if buffer == prefix:
           subprocess.call(['/usr/bin/notify-send', 'In Private Message %s: %s' % (prefix, message)],shell=False)

    elif (ishilight == "1" and
            weechat.config_get_plugin('show_highlight') == "on"):
        buffer = (weechat.buffer_get_string(bufferp, "short_name") or
                weechat.buffer_get_string(bufferp, "name"))
	if os.path.isfile( weechat.config_get_plugin('icon') ):
		subprocess.call(['/usr/bin/notify-send', '-i', weechat.config_get_plugin('icon'), 'In %s %s: %s' % (buffer, prefix, message)],shell=False)
	else:
		subprocess.call(['/usr/bin/notify-send', 'In %s %s: %s' % (buffer, prefix, message)],shell=False)

    return weechat.WEECHAT_RC_OK

