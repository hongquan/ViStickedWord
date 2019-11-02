#!/usr/bin/env python3

import re
import logging
from dataclasses import dataclass
from itertools import chain
from collections import namedtuple
from typing import Match, Tuple, Sequence, List, Optional


__version__ = '0.9'
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

ALL_INITIAL_CONSONANT = frozenset(('b', 'c', 'ch', 'd', 'g', 'gh', 'h', 'kh', 'l', 'm', 'n', 'nh', 'ng',
                                   'ngh', 'p', 'ph', 'q', 'r', 's', 't', 'th', 'v', 'x'))
COMMON_INITIAL_CONSONANT = ALL_INITIAL_CONSONANT - {'gh', 'ngh', 'p', 'q'}

POSSIBLE_INITIAL_CONSONANTS = {
    # "None" means this vowel can start the word. Without "None", it means that
    # this vowel always need an initial consonant.
    'iai': frozenset(['g']),  # "giai". Actually, in this case, "gi" is consonant
    'ieu': COMMON_INITIAL_CONSONANT | {'ngh'} - {'ng', 'gh'},
    'oai': frozenset((None, 'ch', 'h' 'kh', 'l', 't', 'th', 'x')),
    'oao': frozenset(['ng']),
    'oeo': frozenset(['ng']),
    'uay': frozenset(['ng', 'q']),
    'uoi': frozenset(('b', 'c', 'd', 'ch', 'm', 'n', 's', 't', 'x')),
    'uya': frozenset(['kh']),
    'uye': frozenset((None, 'ch', 'ng', 'h', 'kh', 'l', 't', 'q', 't', 'x')),
    'uyu': frozenset(['kh']),
    'ai': COMMON_INITIAL_CONSONANT | {None},
    'ao': COMMON_INITIAL_CONSONANT | {None},
    'eo': COMMON_INITIAL_CONSONANT | {None},
    'ia': frozenset(['g']),
    'ie': COMMON_INITIAL_CONSONANT | {'gh', 'ngh'} - {'c', 'ng'},
    'oa': frozenset((None, 'b', 'ch', 'l', 'n', 't')),
    'oe': frozenset((None, 'kh', 'l', 'nh', 'ng', 'h', 't')),
    'ua': COMMON_INITIAL_CONSONANT | {None, 'q'},
    'ue': frozenset((None, 'h', 'kh', 'q' 't', 'th')),
    'ui': COMMON_INITIAL_CONSONANT | {None, 'q'},
    'uo': frozenset(('ch', 'd', 'kh', 'h', 'l', 'm', 'ng', 'th')),
    'uy': frozenset((None, 'h', 'q')),
    'a': COMMON_INITIAL_CONSONANT | {None},
    'e': ALL_INITIAL_CONSONANT | {None} - {'g', 'ng', 'p', 'q'},
    'i': ALL_INITIAL_CONSONANT | {None} - {'ng', 'q'},
    'o': COMMON_INITIAL_CONSONANT | {None},
    'u': COMMON_INITIAL_CONSONANT | {None},
}

ALL_POSSIBLE_FINAL_CONSONANTS = frozenset(('c', 'ch', 'm', 'n', 'nh', 'ng', 'p', 't', 'th'))

POSSIBLE_FINAL_CONSONANTS = {
    'uye': frozenset(('n', 'nh', 't')),
    # This case, the actual initial consonant is "gi"
    'ia': ALL_POSSIBLE_FINAL_CONSONANTS - {'ch', 'th'},
    'ie': ALL_POSSIBLE_FINAL_CONSONANTS - {'ch', 'th'},
    'oa': ALL_POSSIBLE_FINAL_CONSONANTS - {'th'},
    'oe': frozenset(('n', 't', None)),
    'ua': frozenset(('n', 'ng', 't')),
    'ue': frozenset(['n']),  # quen
    'uo': frozenset(('c', 'm', 'n', 'ng', 't')),
    'uy': frozenset(('ch', 'n', 'nh', 't')),
    'ye': frozenset(('m', 'n', 't')),
    'a': ALL_POSSIBLE_FINAL_CONSONANTS - {'th'},
    'e': ALL_POSSIBLE_FINAL_CONSONANTS - {'nh', 'th'},
    'i': frozenset(('ch', 'm', 'n', 'nh', 'p', 't')),
    'o': frozenset(('c', 'm', 'n', 'ng', 'p', 't')),
    'u': frozenset(('c', 'm', 'n', 'ng', 'p', 't')),
}

ILLEGAL_COMBINATION = {
    'ue': {
        'final': 'n',  # Can only be: quen
        'initial': ALL_INITIAL_CONSONANT - {'q'}
    }
}


def vlen(o: Optional[str]):
    try:
        return len(o)
    except TypeError:
        return 0


def sort_longer(sequence: Sequence[str]) -> Tuple[str]:
    '''Sort list of strings, the longer string will come first'''
    return tuple(sorted(sequence, key=vlen, reverse=True))


POSSIBLE_VOWELS = sort_longer(chain(POSSIBLE_INITIAL_CONSONANTS.keys(),
                                    POSSIBLE_FINAL_CONSONANTS.keys(),
                                    ['y']))
PATTERN_VOWEL = '|'.join(POSSIBLE_VOWELS)
REGEX_VOWEL = re.compile(PATTERN_VOWEL)


_VietSingleWord = namedtuple('_VietSingleWord', ('initial_consonant', 'vowel', 'final_consonant'))


class VietSingleWord(_VietSingleWord):
    @property
    def word(self):
        return f'{self.initial_consonant}{self.vowel}{self.final_consonant}'


@dataclass
class WordPosition:
    start: int = 0
    end: int = 0
    start_vowel: int = 0
    end_vowel: int = 0
    # When failed to find suitable initial consonant, we may negotiate with precedence word
    # to get some letter from it
    should_negotiate_precedence: bool = False


def build_word(p: WordPosition, original_word_sequence: str) -> VietSingleWord:
    vowel = original_word_sequence[p.start_vowel:p.end_vowel]
    initial_consonant = original_word_sequence[p.start:p.start_vowel]
    final_consonant = original_word_sequence[p.end_vowel:p.end]
    return VietSingleWord(
        initial_consonant=initial_consonant,
        vowel=vowel,
        final_consonant=final_consonant
    )


def scan_for_word(i: int, vowel_match: Match, vowel_occurences: Sequence[Match],
                  word_positions: List[WordPosition], original_word_sequence: str) -> WordPosition:
    '''Scan for initial and final consonant, determine position of components in original word sequences'''
    vowel = vowel_match.group(0)
    pos_start_vowel = vowel_match.start(0)
    pos_end_vowel = vowel_match.end(0)
    word_pos = WordPosition(start=pos_start_vowel, end=pos_end_vowel,
                            start_vowel=pos_start_vowel, end_vowel=pos_end_vowel)
    # Look for initial consonant
    try:
        test_consonants = sort_longer(POSSIBLE_INITIAL_CONSONANTS[vowel])
        try:
            prev_word = word_positions[i - 1]
            start_scan = prev_word.end
        except IndexError:
            start_scan = 0
        leading_part = original_word_sequence[start_scan:pos_start_vowel]
        for con in test_consonants:
            if con is not None and leading_part.endswith(con):
                # Found initial consonant
                word_pos.start = pos_start_vowel - len(con)
                break
        else:
            # Possible consonant for this vowel doesn't match the leading part.
            logger.error('Confused. Leading part "%s" does not seem to be initial consonant of "%s"',
                         leading_part, vowel)
            word_pos.start -= len(leading_part)
            word_pos.should_negotiate_precedence = True
    except KeyError:
        # No need initial consonant
        pass
    # Look for final consonant
    try:
        test_consonants = sort_longer(POSSIBLE_FINAL_CONSONANTS[vowel])
        rest_seq = original_word_sequence[pos_end_vowel:]
        for con in test_consonants:
            if con is not None and rest_seq.startswith(con):
                # Determined final consonant of this word
                word_pos.end = pos_end_vowel + len(con)
                break
        else:
            # No final consonant
            pass
    except KeyError:
        # This vowel doesn't need final consonant
        pass
    # May resolve confusion be get more letter from precedence word
    # Here: "ngoenguay" is split to ("ngoen", "guay").
    # We will take letters from "ngoen", preprending to "guay"
    if word_pos.should_negotiate_precedence:
        negotiate_expand_consonant(word_pos, word_positions, original_word_sequence)
    # Save position of this word
    word_positions.append(word_pos)
    return word_pos


def negotiate_expand_consonant(word_pos: WordPosition, word_positions: List[WordPosition],
                               original_word_sequence: str) -> Tuple[WordPosition]:
    # Example: "ngoenguay" is split to ("ngoen", "guay").
    # We will take letters from "ngoen", preprending to "guay" to get better result
    try:
        prev_pos = word_positions[-1]
        prev_vowel = original_word_sequence[prev_pos.start_vowel:prev_pos.end_vowel]
        vowel = original_word_sequence[word_pos.start_vowel:word_pos.end_vowel]
        test_initial_consonants = sort_longer(POSSIBLE_INITIAL_CONSONANTS[vowel])
        test_final_consonants = sort_longer(POSSIBLE_FINAL_CONSONANTS[prev_vowel])
        logger.debug('Loop i over %s', tuple(range(prev_pos.end - 1, prev_pos.end_vowel - 1, -1)))
        for i in range(prev_pos.end - 1, prev_pos.end_vowel - 1, -1):
            expanded_consonant = original_word_sequence[i:word_pos.start_vowel] or None
            shrunk_consonant = original_word_sequence[prev_pos.end_vowel:i] or None
            if expanded_consonant in test_initial_consonants and shrunk_consonant in test_final_consonants:
                # Negotiated
                word_pos.start = i
                prev_pos.end = i
                return prev_pos, word_pos
        else:
            # Negotiation failed
            logger.error('Negotiation failed.')
    except IndexError:
        logger.error('Previous word does not exist.')
    except KeyError:
        logger.error('Previous word doesnot need final consonant')


def parse(wordseq: str):
    logger.debug('Regex: %s', REGEX_VOWEL)
    occurences: Sequence[Match] = tuple(REGEX_VOWEL.finditer(wordseq))
    logger.debug('Vowel occurences: %s', occurences)
    word_positions: List[WordPosition] = []
    for i, match in enumerate(occurences):
        scan_for_word(i, match, occurences, word_positions, wordseq)
    return tuple(build_word(p, wordseq) for p in word_positions)


def split_words(string: str) -> Tuple[str]:
    return tuple(w.word for w in parse(string))
