#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file name: ''tweetdecayopts.py''
# project: Tweet Decay
#
# function: Options for tweetdecay.py
#
# last change: $LastChangedRevision$
#
# Copyright (C) 2010,2011 Robert Lange <sd2k9@sethdepot.org>
# Licensed under the GNU General Public License, version 2
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
#



# *** Twitter Account Information
# You need to register this application to your twitter account
# to allow it's access
# - Log into your account
# - Go to Settings/Developer Applications (https://twitter.com/apps)
# - Register a new applicaton
# - Fill the data; Suggestions
#   Application Name: tweetdecay
#   Description: Automatically removes tweets older than a certain time
#   Applicaton Website: https://github.com/sd2k9/tweetdecay
#   Application Type: Client
#   Default Access type: Read & Write
#   Use Twitter for login: Yes (checked)
# - Then fill consumer_key and consumer_secret with the supplied data
# - Execute program ./get_access_tokey.py to retrieve the
#   access_token_* data and fill it here also
twitteraccount = {
            'consumer_key': '',
            'consumer_secret': '',
            'access_token_key': '',
            'access_token_secret': ''
       }


# *** Global settings
opts = { # Decay time in days: Remove tweets older than this
         'decaytime': 10,
         #
         # The following settings are used internally, so
         # you cannot change them here. They are only listed for convenience.
         # testmode - Test Mode / Dry Run
         # 'testmode': True,
       }

# *** Settings for tweetfile link removal
tweetfile = {
        # Enable or Disable tweetfile link removal
        # 'enable': True,
        'enable': False,
        # Url base of tweetfile, take from tweetfileaccess.py entry "fileurlbase"
        'linkbase': 'http://server.org/tweetfile/myuser',
        # The ssh account you use with ssh to access your server
        'sshaccount': 'tweeter@server.org',
        # Directory where the tweetfiles are to be found on the remote server
        'filebase': '/srv/www/vhost/vhost5/tweetfile/myuser',
    }

# *** Settings for URL shorteners
urlshorten = {
   'bitly': {     # Bitly URL Shortener's API required login
        # You can get it from here: https://bit.ly/a/your_api_key
        # Enable or Disable bitly link resolution
        # 'enable': True,
        'enable': False,
        #  bit.ly URL shortener user name and API key
        'api_user' : None,
        'api_key' : None,
    }
}
