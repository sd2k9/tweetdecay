#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file name: ''tweetdecayopts.py''
# project: Tweet Decay
#
# function: Options for tweetdecay.py
#
# last change: $LastChangedRevision$
#
# Copyright (C) 2010,2011 Robert Lange (robert.lange@s1999.tu-chemnitz.de)
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
       }
