#!/usr/bin/env python3
# coding=utf-8
import json
import sys
import tempfile
from copy import copy
from random import shuffle


def read_json_file(filename, encoding):
    with open(filename, "r", encoding=encoding) as file:
        return json.loads(file.read())


def generate_alphabet_list(start, end):
    return [x for x in map(chr, range(ord(start), ord(end) + 1))]


def create_aplhabet(string):
    """
    Создание листа из промежутка букв
    """
    letter_range = "".join(
        x for x in string if x.islower() or x == '-').strip('-')
    if len(letter_range) == 3:
        return generate_alphabet_list(letter_range[0], letter_range[2])
    defis = letter_range.find('-')
    alphabet = generate_alphabet_list(letter_range[defis - 1], letter_range[defis + 1])
    for letter in letter_range:
        if letter_range.find(letter) not in range(defis - 1, defis + 2):
            alphabet.append(letter)
    return alphabet


def generate_substitution(string):
    """
    Создание новой перестановки из алфавита
    """
    alphabet = create_aplhabet(string)
    shuffled = copy(alphabet)
    shuffle(shuffled)
    return dict(zip(alphabet, shuffled))
    
def reverse_substitution(substitution):
    return {v: k for k, v in substitution.items()}



def code_text_from_file(filename, encoding, substitution):
    with open(filename, 'r', encoding='utf-8') as file:
        return code(file.read(), substitution)


def code(text, substitution):
    """
    Перевод текста путем сопоставления одной буквы другой.
    """
    upper_letters = dict(zip([x.upper() for x in substitution.keys()],
                             [x.upper() for x in substitution.values()]))
    tab = str.maketrans(dict(substitution, **upper_letters))
    return text.translate(tab)
