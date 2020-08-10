#!/usr/bin/env python3

import re
import logging
from pathlib import Path
from dataclasses import dataclass
from itertools import chain
from collections import namedtuple
from typing import Match, Tuple, Sequence, List, Optional

from single_version import get_version


__version__ = get_version('vistickedword', Path(__file__).parent)
logger = logging.getLogger(__name__)

ALL_INITIAL_CONSONANT = frozenset(('b', 'c', 'ch', 'd', 'g', 'gh', 'h', 'kh', 'l', 'm', 'n', 'nh', 'ng',
                                   'ngh', 'p', 'ph', 'q', 'r', 's', 't', 'th', 'tr', 'v', 'x'))
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
    'uoi': frozenset(('b', 'c', 'd', 'ch', 'm', 'n', 'ng', 's', 't', 'x')),
    'uya': frozenset(['kh']),
    'uye': frozenset((None, 'ch', 'ng', 'h', 'kh', 'l', 't', 'q', 't', 'x')),
    'uyu': frozenset(['kh']),
    'ai': COMMON_INITIAL_CONSONANT | {None},
    'ao': COMMON_INITIAL_CONSONANT | {None},
    'eo': COMMON_INITIAL_CONSONANT | {'ngh', 'gh', None},
    'eu': COMMON_INITIAL_CONSONANT,
    'ia': frozenset(['g']),
    'ie': COMMON_INITIAL_CONSONANT | {'gh', 'ngh'} - {'c', 'ng'},
    'io': frozenset(['g']),
    'iu': frozenset(('ch', 'b', 'd', 'g', 'l', 'm', 'n', 'r', 't', 'th', 'x')),
    'oa': frozenset((None, 'b', 'ch', 'h', 'kh', 'l', 'n', 'ng', 't')),
    'oe': frozenset((None, 'kh', 'l', 'nh', 'ng', 'h', 't')),
    'ua': COMMON_INITIAL_CONSONANT | {None, 'q'},
    'ue': frozenset((None, 'h', 'kh', 'q' 't', 'th')),
    'ui': COMMON_INITIAL_CONSONANT | {None, 'q'},
    'uo': COMMON_INITIAL_CONSONANT | {None},
    'uu': COMMON_INITIAL_CONSONANT | {None},
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
    'ia': ALL_POSSIBLE_FINAL_CONSONANTS - {'ch', 'th', None},
    'ie': ALL_POSSIBLE_FINAL_CONSONANTS - {'ch', 'th'},
    'oa': ALL_POSSIBLE_FINAL_CONSONANTS | {None} - {'th'},  # m: "oai oam"
    'oe': frozenset(('n', 't', None)),
    'ua': frozenset(('m', 'n', 'ng', 't', None)),   # m: "dao quam"
    'ue': frozenset(('n', None)),  # quen, que
    'uo': frozenset(('c', 'm', 'n', 'ng', 'p', 't', None)),
    'uy': frozenset(('ch', 'n', 'nh', 't', None)),
    'ye': frozenset(('m', 'n', 't')),
    'a': ALL_POSSIBLE_FINAL_CONSONANTS | {None} - {'th'},
    'e': ALL_POSSIBLE_FINAL_CONSONANTS | {None} - {'nh', 'th'},
    'i': frozenset(('ch', 'm', 'n', 'nh', 'p', 't', None)),
    'o': frozenset(('c', 'm', 'n', 'ng', 'p', 't', None)),
    'u': frozenset(('c', 'm', 'n', 'ng', 'p', 't', None)),
}

ILLEGAL_COMBINATION = {
    'ue': (
        {
            'final': 'n',  # Can only be: quen
            'initial': ALL_INITIAL_CONSONANT - {'q'}
        },
    ),
    'oa': (
        {
            'final': 'm',  # Can only be: oam
            'initial': ALL_INITIAL_CONSONANT,
        },
    ),
    'ua': (
        {
            'final': 'ng',
            'initial': ALL_INITIAL_CONSONANT - {'kh'}
        },
    )
}


def vlen(o: Optional[str]) -> int:
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


class IllegalCombination(ValueError):
    pass


class ConfusingState(ValueError):
    pass


def build_word(p: WordPosition, original_word_sequence: str) -> VietSingleWord:
    vowel = original_word_sequence[p.start_vowel:p.end_vowel]
    initial_consonant = original_word_sequence[p.start:p.start_vowel]
    final_consonant = original_word_sequence[p.end_vowel:p.end]
    return VietSingleWord(
        initial_consonant=initial_consonant,
        vowel=vowel,
        final_consonant=final_consonant
    )


def find_initial_consonant(vowel: str, final_consonant: str,
                           leading_source: str, test_initial_consonants: Sequence[str]) -> str:
    for con in test_initial_consonants:
        if con is not None and leading_source.lower().endswith(con.lower()):
            # Found initial consonant
            initial_consonant = con
            break
    # Not found initial consonant from leading source
    else:
        logger.error('Not found initial consonant for "%s" from "%s"', vowel, leading_source)
        raise ConfusingState
    if not final_consonant:
        return initial_consonant
    # Check if this combination is illegal
    if vowel in ILLEGAL_COMBINATION:
        illegal_combinations = ILLEGAL_COMBINATION[vowel]
        prohibited = (c['initial'] for c in illegal_combinations if c['final'] == final_consonant)
        illegal_initials = next(prohibited, ())
        if initial_consonant.lower() in illegal_initials:
            logger.error('Combination of ("%s", "%s", "%s") is illegal.',
                         initial_consonant, vowel, final_consonant)
            raise IllegalCombination
    return initial_consonant


def scan_for_word(i: int, vowel_match: Match, vowel_occurences: Sequence[Match],
                  word_positions: List[WordPosition], original_word_sequence: str) -> WordPosition:
    '''Scan for initial and final consonant, determine position of components in original word sequences'''
    vowel = vowel_match.group(0)
    pos_start_vowel = vowel_match.start(0)
    pos_end_vowel = vowel_match.end(0)
    word_pos = WordPosition(start=pos_start_vowel, end=pos_end_vowel,
                            start_vowel=pos_start_vowel, end_vowel=pos_end_vowel)
    final_consonant = None
    try:
        test_initial_consonants = sort_longer(POSSIBLE_INITIAL_CONSONANTS[vowel])
    except KeyError:
        test_initial_consonants = ()
    try:
        prev_word = word_positions[i - 1]
        start_scan = prev_word.end
    except IndexError:
        start_scan = 0
    leading_source = original_word_sequence[start_scan:pos_start_vowel]

    # We determine final consonant first, because some initial consonants are valid or invalid subject to final one.
    # Look for final consonant
    try:
        test_final_consonants = sort_longer(POSSIBLE_FINAL_CONSONANTS[vowel])
    except KeyError:
        # This vowel doesn't need final consonant
        test_final_consonants = ()

    rest_seq = original_word_sequence[pos_end_vowel:]
    final_consonant = None
    # If rest_seq is empty, no need to scan for final consonant
    if rest_seq:
        for con in test_final_consonants:
            if con is None:
                logger.debug('This vowel "%s" can go without final consonant', vowel)
                word_pos.end = word_pos.end_vowel
                break
            if rest_seq.lower().startswith(con.lower()):
                # Determined final consonant of this word
                final_consonant = con
                word_pos.end = pos_end_vowel + len(final_consonant)
                if not leading_source:
                    logger.debug("No pool to find initial consonant")
                    break
                if test_initial_consonants:
                    try:
                        initial_consonant = find_initial_consonant(vowel, final_consonant, leading_source,
                                                                   test_initial_consonants)
                    except ConfusingState:
                        word_pos.start = word_pos.start_vowel - len(leading_source)
                        success = negotiate_expand_consonant(word_pos, word_positions, original_word_sequence)
                        if not success:
                            continue
                        else:
                            break
                    except IllegalCombination:
                        logger.debug("Illegal combination. Test next possible final consonant.")
                        continue
                    word_pos.start = pos_start_vowel - len(initial_consonant)
                break
    # Not found final consonant
    if not final_consonant and test_final_consonants and None not in test_final_consonants:
        logger.error('This vowel "%s" needs a final consonant, but could not found in "%s".',
                     vowel, rest_seq)
    # Even when final consonant is not needed, still need to find initial
    elif leading_source:
        try:
            initial_consonant = find_initial_consonant(vowel, None, leading_source,
                                                       test_initial_consonants)
            word_pos.start = pos_start_vowel - len(initial_consonant)
        except ConfusingState:
            word_pos.start = word_pos.start_vowel - len(leading_source)
            negotiate_expand_consonant(word_pos, word_positions, original_word_sequence)
    elif None not in test_initial_consonants:
        # This vowel needs initial consonant
        logger.debug('Vowel "%s" needs an initial consonant. Negotiate with precedence word.', vowel)
        negotiate_expand_consonant(word_pos, word_positions, original_word_sequence)
    else:
        logger.debug("Skip finding initial consonant for %s.", vowel_match)
    # Save position of this word
    word_positions.append(word_pos)
    return word_pos


def negotiate_expand_consonant(word_pos: WordPosition, word_positions: List[WordPosition],
                               original_word_sequence: str) -> bool:
    # Example: "ngoenguay" is split to ("ngoen", "guay").
    # We will take letters from "ngoen", preprending to "guay" to get better result
    try:
        prev_pos = word_positions[-1]
        prev_vowel = original_word_sequence[prev_pos.start_vowel:prev_pos.end_vowel]
        vowel = original_word_sequence[word_pos.start_vowel:word_pos.end_vowel]
        test_initial_consonants = sort_longer(POSSIBLE_INITIAL_CONSONANTS[vowel])
        test_final_consonants = sort_longer(POSSIBLE_FINAL_CONSONANTS[prev_vowel])
        for i in range(prev_pos.end - 1, prev_pos.end_vowel - 1, -1):
            expanded_consonant = original_word_sequence[i:word_pos.start_vowel] or None
            shrunk_consonant = original_word_sequence[prev_pos.end_vowel:i] or None
            if expanded_consonant in test_initial_consonants and shrunk_consonant in test_final_consonants:
                # Negotiated
                word_pos.start = i
                prev_pos.end = i
                return True
        else:
            # Negotiation failed
            logger.error('Negotiation failed.')
    except IndexError:
        logger.error('Previous word does not exist.')
    except KeyError as e:
        logger.error('Vowel %s cannot go with initial consonant', e)
    return False


def parse(wordseq: str):
    occurences: Sequence[Match] = tuple(REGEX_VOWEL.finditer(wordseq.lower()))
    logger.debug('Vowel occurences: %s', occurences)
    word_positions: List[WordPosition] = []
    for i, match in enumerate(occurences):
        scan_for_word(i, match, occurences, word_positions, wordseq)
    return tuple(build_word(p, wordseq) for p in word_positions)


def split_words(string: str) -> Tuple[str]:
    return tuple(w.word for w in parse(string))
