#!/usr/bin/env python3

import re
from typing import Match, Iterator, Tuple

#-------- Thinking ----------#

# This part is not used in code. Just to let me revisit how the Vietmese word structure looks like, to give idea how to parse it.

INITIAL_CONSONANT = ('b', 'c', 'ch', 'd', 'g', 'gh', 'k', 'kh', 'l', 'm', 'n', 'ng', 'p', 'ph',
                     'q', 'r', 's', 't', 'th', 'v', 'x', 'y')

FINAL_CONSONANT = ('c', 'ch', 'm', 'n', 'ng', 'nh', 't', 'th')


PAT_INITIAL_CONSONANT = r'[bcdgklmnpqrstvx](?:(?<=n)g)?(?:(?<=[cgkpt])h)?(?=[aeiou])'
PAT_VOWEL = r'[aeiou]+'
PAT_FINAL_CONSONANT = r'(?<=[aeiou])[cmnt](?:(?<=[cnt])h)?'

REGEX_INITIAL_CONSONANT = re.compile(PAT_INITIAL_CONSONANT)
REGEX_VOWEL = re.compile(PAT_VOWEL)
REGEX_FINAL_CONSONANT = re.compile(PAT_FINAL_CONSONANT)

# ----- Actual code ----- #

REGEX_WORD = re.compile(r'(?P<initial_consonant>[bcdghklmnpqrstvxy]*((?<=n)g)?((?<=[cgkpt])h)?)'
                        r'(?P<vowel>oai|uoi|uye|uya|ieu|uay|oeo|uyu'
                        r'|ai|ao|au|ay|eo|eu|ia|ie|iu|oa|oe|oi|sua|ue|ui|uo|uy|[aeiouy])'
                        r'(?P<final_consonant>[cmnt]?((?<=[cnt])h|(?<=n)g)?)', re.IGNORECASE)


def iter_split_words(string: str) -> Iterator[Match]:
    return REGEX_WORD.finditer(string)


def split_words(string: str) -> Tuple[str]:
    return tuple(m.group(0) for m in iter_split_words(string))
