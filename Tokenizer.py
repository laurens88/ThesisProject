#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code implements a basic, Twitter-aware tokenizer.

A tokenizer is a function that splits a string of text into words. In
Python terms, we map string and unicode objects into lists of unicode
objects.

There is not a single right way to do tokenizing. The best method
depends on the application.  This tokenizer is designed to be flexible
and this easy to adapt to new domains and tasks.  The basic logic is
this:

1. The tuple regex_strings defines a list of regular expression
   strings.

2. The regex_strings strings are put, in order, into a compiled
   regular expression object called word_re.

3. The tokenization is done by word_re.findall(s), where s is the
   user-supplied string, inside the tokenize() method of the class
   Tokenizer.

4. When instantiating Tokenizer objects, there is a single option:
   preserve_case.  By default, it is set to True. If it is set to
   False, then the tokenizer will downcase everything except for
   emoticons.

The __main__ method illustrates by tokenizing a few examples.

I've also included a Tokenizer method tokenize_random_tweet(). If the
twitter library is installed (http://code.google.com/p/python-twitter/)
and Twitter is cooperating, then it should tokenize a random
English-language tweet.
"""

__author__ = "Christopher Potts"
__copyright__ = "Copyright 2011, Christopher Potts"
__credits__ = []
__license__ = "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License: " \
              "http://creativecommons.org/licenses/by-nc-sa/3.0/"
__version__ = "1.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the author's website"

######################################################################

import re
import html.entities

######################################################################
# The following strings are components in the regular expression
# that is used for tokenizing. It's important that phone_number
# appears first in the final regex (since it can contain whitespace).
# It also could matter that tags comes after emoticons, due to the
# possibility of having text like
#
#     <:| and some text >:)
#
# Most imporatantly, the final element should always be last, since it
# does a last ditch whitespace-based tokenization of whatever is left.

# This particular element is used in a couple ways, so we define it
# with a name:
emoticon_string = r"""
    (?:
      [<>]?
      [:;=8]                     # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[/\:\}\{@\|\\] # mouth
    )"""

# The components of the tokenizer:
regex_strings = (
    # Emoticons:
    emoticon_string
    ,
    # Dates
    r"""(?:\d+[\/|-]\d+[\/|-]\d+)"""

    ,
    # Time in hh:mm(:ss) format
    r"""(?:\d+:\d+:?\d{0,2})"""
    ,
    # URLs
    r"""http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"""
    ,
    # HTML tags:
    r"""<[^>]+>"""
    ,
    # Twitter username:
    r"""(?:@[\w_]+)"""

    ,
    # Twitter cashtags
    r"""(?:\$[a-zA-Z]+)"""
    ,

    # Percentages
    r"""(?:[+|-]*\d+[,|.]?\d*[,|.]?\d*\%)"""

    ,
    # Prices in $42k, 42K  format
    r"""(?:\$?\d+[,|.]?\d*[k|K])"""

    ,
    # Prices (starting or ending with a dollar sign)
    r"""(?:\$?\d+[,|.]?\d*[,|.]?\d*[,|.]?\d*[,|.]?\d*\$?)"""

    ,
    # Time in hh:mm(:ss) format
    r"""(?:\d+:\d+:?\d{0,2})"""

    ,
    # Dates
    r"""(?:\d+[\/|-]\d+[\/|-]\d+)"""

    ,
    # Twitter hashtags:
    r"""(?:\#+[\w_]+[\w\'_\-]*[\w_]+)"""
    ,
    # Remaining word types:
    r"""
    (?:[a-z][a-z'\-_]+[a-z])       # Words with apostrophes or dashes.
    |
    (?:[+\-]?\d+[,/.:-]\d+[+\-]?)  # Numbers, including fractions, decimals.
    |
    (?:[\w_]+)                     # Words without apostrophes or dashes.
    |
    (?:\.(?:\s*\.){1,})            # Ellipsis dots. 
    |
    (?:\S)                         # Everything else that isn't whitespace.
    """
)

######################################################################
# This is the core tokenizing regex:

word_re = re.compile(r"""(%s)""" % "|".join(regex_strings), re.VERBOSE | re.I | re.UNICODE)

# The emoticon string gets its own regex so that we can preserve case for them as needed:
emoticon_re = re.compile(regex_strings[1], re.VERBOSE | re.I | re.UNICODE)

# These are for regularizing HTML entities to Unicode:
html_entity_digit_re = re.compile(r"&#\d+;")
html_entity_alpha_re = re.compile(r"&\w+;")
amp = "&amp;"

######################################################################


class Tokenizer:
    def __init__(self, preserve_case=False):
        self.preserve_case = preserve_case

    def tokenize(self, string):
        """
        Argument: s -- any string or unicode object
        Value: a tokenize list of strings; conatenating this list returns the original string if preserve_case=False
        """
        # Try to ensure unicode:
        try:
            string = str(string)
        except UnicodeDecodeError:
            string = str(string).encode('string_escape')
            string = str(string)
        # Fix HTML character entitites:
        string = self.html2unicode(string)
        # Tokenize:
        words = word_re.findall(string)
        # Possible alter the case, but avoid changing emoticons like :D into :d:
        if not self.preserve_case:
            words = map((lambda x: x if emoticon_re.search(x) else x.lower()), words)
        return words

    def html2unicode(self, string):
        """
        Internal metod that seeks to replace all the HTML entities in
        s with their corresponding unicode characters.
        """
        # First the digits:
        ents = set(html_entity_digit_re.findall(string))
        if len(ents) > 0:
            for ent in ents:
                entnum = ent[2:-1]
                try:
                    entnum = int(entnum)
                    string = string.replace(ent, chr(entnum))
                except:
                    pass
        # Now the alpha versions:
        ents = set(html_entity_alpha_re.findall(string))
        ents = filter((lambda x: x != amp), ents)
        for ent in ents:
            entname = ent[1:-1]
            try:
                string = string.replace(ent, chr(html.entities.name2codepoint[entname]))
            except:
                pass
            string = string.replace(amp, " and ")
        return string

###############################################################################


if __name__ == '__main__':
    tok = Tokenizer(preserve_case=False)
    samples = (
        u"RT @ #happyfuncoding: this is a typical Twitter tweet :-)",
        u"HTML entities &amp; other Web oddities can be an &aacute;cute <em class='grumpy'>pain</em> >:(",
        u"It's perhaps noteworthy that phone numbers like +1 (800) 123-4567, (800) 123-4567, and 123-4567 are treated as words despite their whitespace."
    )

    for s in samples:
        print("======================================================================")
        print(s)
        tokenized = tok.tokenize(s)
        print("\n".join(tokenized))
