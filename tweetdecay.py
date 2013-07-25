#!/usr/bin/env python
# -*- coding: utf-8 -*-
# file name: ''tweetdecay.py''
# project: Tweet Decay
#
# function: Automatically delete twitter tweets with a certain age
#
# last change: $LastChangedRevision$
#
#    Copyright (C) 2010,2011 Robert Lange (robert.lange@s1999.tu-chemnitz.de)
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#


# *** Import modules
# Regular Expression Service
import re
# Time conversion
# from datetime import datetime
# To control output level easily
# from __future__ import print_function
import logging
# Argument parser
import optparse
# Twitter interface
import twitter
# Time manipulation
import datetime
import rfc822
# Bitly API
import bitly
# Required to resolve t.co links
import urllib2
# exit et al
import sys


# *** Get the options
import tweetdecayopts

# *** Provide logging shortcuts
pinfo  = logging.info
pwarn  = logging.warning
perror = logging.error




# ********************************************************************************

# *** Twitter messager class
class tweetkiller:
    """Delete tweets older than a certain time"""

    # Variables
    _api = ""

    def __init__(self):
        """C'tor: Create Twitter API object"""
        # Username/password: Consumer Data, not account
        # access_*: Fetch from tool python-twitter/get_access_token.py
        self._api = twitter.Api(consumer_key=tweetdecayopts.twitteraccount['consumer_key'],
                      consumer_secret=tweetdecayopts.twitteraccount['consumer_secret'],
                      access_token_key=tweetdecayopts.twitteraccount['access_token_key'],
                      access_token_secret=tweetdecayopts.twitteraccount['access_token_secret']
                                )
        # Debug:
        # print self._api.VerifyCredentials()

    def decay(self, decaytime):
       """Remove tweets older than decaytime in days"""
       pinfo("Removing tweets older than " + str(decaytime) +" days")

       # Create date time object, substracted the keeping time so we can use it
       # to decide which tweet to remove
       tdecay = datetime.datetime.now() - \
               datetime.timedelta(tweetdecayopts.opts['decaytime'])
       pinfo("   Will remove all tweets before " + tdecay.strftime("%Y-%m-%d") + \
                 " (older than "+ str(tweetdecayopts.opts['decaytime']) + " days)")

       # Get all tweets
       tweets = self._api.GetUserTimeline(count=200)

       # Debug: Print all tweets
       print "\n".join(["   " + s.text + "\n      " + s.created_at + " " + str(s.id) \
                        for s in tweets])

       # RE object for plixi link detection
       # Template: eted http://plixi.com/p/64347208 (not per
       re_plixi = re.compile("(?:[^\s]\s+)?http://plixi.com/p/(\d+)\s*")
       # RE object for other link detection (usually after URL shortener)
       # Template: eted http://something else but not plixi
       re_link = re.compile("(?:[^\s]\s+)?(http://[\w\d\./]+)[\s+.*]?$")

       # Decide which tweets will be removed
       for it in tweets:
           # Template for time: Fri Dec 17 09:09:10 +0000 2010
           if datetime.datetime(*(rfc822.parsedate(it.created_at))[0:6]) < tdecay:
               # For plixi-Link try also to remove the picture
               re_match = re_plixi.search(it.text)
               if re_match is not None:
                   self._remove_plixi(re_match.group(1))
               else:
                   # For other link process this further
                   re_match = re_link.search(it.text)
                   if re_match is not None:
                       self._remove_link(re_match.group(1))
               # Do the actual removal of the tweet
               self._remove_tweet(it)

    def _remove_tweet(self, tweet):
       """Remove this tweet (private function)"""
       # Signal testmode also in message
       if tweetdecayopts.opts['testmode']:
           testmode = " (not performed in testmode)"
       else:
           testmode = ""

       # Show work to be done
       pinfo("   Remove Tweet: "+ tweet.text + testmode + "\n         " + tweet.created_at + " " + str(tweet.id))

       # Remove, when not testmode
       if not tweetdecayopts.opts['testmode']:
           # DEBUG TO AVOID ACCIDENTAL DELETE
           # pass
           self._api.DestroyStatus(tweet.id)

    def _remove_plixi(self, pid):
       """Remove this plixi ID picture (private function)"""

       # Signal testmode also in message
       if tweetdecayopts.opts['testmode']:
           testmode = " (not performed in testmode)"
       else:
           testmode = ""

       # Show work to be done
       pinfo("   Remove Plixi Image: "+ pid + testmode)

       # Remove, when not testmode
       if not tweetdecayopts.opts['testmode']:
           perror("NOT IMPLEMENTED YET (and won't happen)")
           pass    # not implemented yet

    def _remove_link(self, link):
       """Remove this link (private function)

       Does link expansion and hands over to correct removal function.
       """

       # Signal testmode also in message
       if tweetdecayopts.opts['testmode']:
           testmode = " (not performed in testmode)"
       else:
           testmode = ""

       # Show work to be done
       pinfo("   Check for link removal: "+ link + testmode)

       # First check, are we behind any known URL shortener?
       # Currently we only know bit.ly
       if tweetdecayopts.urlshorten['bitly']['enable'] is True and \
          re.search("^http://bit.ly/\w+$", link):
           # Yes, bitly expansion needed
           bitlyworker=bitly.Api(login= tweetdecayopts.urlshorten['bitly']['api_user'], apikey= tweetdecayopts.urlshorten['bitly']['api_key'])
           link = bitlyworker.expand(link)
           pinfo("   Expanded URL via bit.ly: "+ link + testmode)

       # And also t.co links - soon
       
       # Thanks goes to: http://stackoverflow.com/questions/8872232/unwrap-t-co-links-with-python
       # req = urllib2.urlopen(tco_url)
       # print req.url

       # Then check that we're a tweetfile link
       if tweetdecayopts.tweetfile['enable'] is True:
           lmatch = re.search("^" + tweetdecayopts.tweetfile['linkbase'] + "/?([^/].*)$", link)
           if lmatch is not None:
               # Yes, again hand over work
               self._remove_link_tweetfile(lmatch.group(1), testmode)
           else:
               pinfo("      No tweetfile link - ignoring")

    def _remove_link_tweetfile(self, link, testmode):
       """Remove this link created by tweetfile (private function)

       1.P: tweetfile link, linkbase removed
       2.P: String to expand on outputs to signal testmode when enabled
       """

       # Show work to be done
       pinfo("   Detected tweetfile link to remove: "+ link + " (base stripped)" + testmode)

       # Remove, when not testmode
       if not tweetdecayopts.opts['testmode']:
           cmd = ["ssh", tweetdecayopts.tweetfile['ssh_account'], "rm", \
                      tweetdecayopts.tweetfile['filebase'] + link ]
           pinfo("   Executing " + cmd + "...")
           try:
               retcode = subprocess.call(cmd, shell=False)
               if retcode < 0:
                   print "cmd was terminated by signal" + str(-retcode)
               elif retcode > 0:
                   print "cmd returned error code " + str(retcode)
           except OSError, e:
               print "cmd execution failed: " + str(e)
               raise
           except:
               raise   # Other errors are passed further

       # Done
       return


    def finish(self):
        """Destructor - Cleanup"""
        self._api.ClearCredentials()


# ********************************************************************************

# *** Main Program
def main():

    # Variables
    # ...

    # Command line parsing: QUIET option and Test Run
    cmd_usage="usage: %prog [options] args"
    cmd_desc ="""TODO WRITE ME"""
    cmd_version="%prog " + __version__
    cmd_parser = optparse.OptionParser(usage=cmd_usage,
                                   description=cmd_desc, version=cmd_version)
    cmd_parser.add_option('-V', action='version', help=optparse.SUPPRESS_HELP)
    cmd_parser.add_option('--quiet', '-q', dest='quiet', action='store_true',
                        default=False, help='Quiet Output')
    cmd_parser.add_option('--dry-run', '--test', '-t', dest='test', action='store_true',
                        default=False, help='Dry Run, only echo deletion tasks without performing them')
    # more options to add
    (cmd_opts, cmd_args) = cmd_parser.parse_args()

    # Setup logging: Show only from warnings when being QUIET
    logging.basicConfig(level=logging.WARNING if cmd_opts.quiet else logging.INFO,
                    format="%(message)s")

    # Report Testing mode if set
    tweetdecayopts.opts['testmode'] = cmd_opts.test # Make available for everyone
    if cmd_opts.test:
        pinfo("Test mode selected, deletion will NOT be performed")

    # Abort when different than no argument
    if len(cmd_args) != 0:
        perror("No command line arguments are expected!")
        cmd_parser.print_usage()
        return 1

    # Now just hand over work to the tweetkiller object
    twitkill = tweetkiller()       # Create new object
    twitkill.decay(tweetdecayopts.opts['decaytime'])  # Do the work
    pinfo("Tweet Decay done")
    twitkill.finish()    # Cleanup

    # Done we are
    return 0



# *** Call Main program
__version__ = ''.join(filter(str.isdigit, "$LastChangedRevision$"))
if __version__ == "":
   __version__ = "(development version)"
if __name__ == "__main__":
    sys.exit(main())
