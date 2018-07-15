#!/usr/bin/env python3
# coding=utf-8
import json
import os
import sys
import random
from copy import copy
from itertools import groupby
from random import shuffle
from logic.learner import TextInfo
from logic.encryptor import code_text_from_file, create_aplhabet, generate_substitution, code
from collections import OrderedDict
workdone = 0


def generate_alphabet_list(start, end):
    """
    Создание листа, содержащего все буквы от начала до конца
    """
    return [x for x in map(chr, range(ord(start), ord(end) + 1))]


def get_pattern(word):
    """
    Создание паттерна - пример '0123412356' для 'DUSTBUSTER'
    """
    next_num = 0
    letter_nums = {}
    word_mask = []
    for letter in word:
        if letter not in letter_nums:
            letter_nums[letter] = str(next_num)
            next_num += 1
        word_mask.append(letter_nums[letter])
    return ''.join(word_mask)


def get_wordlists_pattern(words):
    """
    Создание паттерна для всех слов в листе.
    """
    all_masks = {}
    for word in words:
        mask = get_pattern(word)
        if mask not in all_masks:
            all_masks[mask] = [word]
        else:
            all_masks[mask].append(word)
    return all_masks


def create_default_substitution(alph):
    """
    Создание стандартной подстановки из алфавита
    """
    return {letter: set() for letter in create_aplhabet(alph)}


def expand_substitution(substitution, cipher_word, word):
    """
    Поиск подходящих букв
    """
    substitution = copy(substitution)
    for i in range(len(cipher_word)):
        substitution[cipher_word[i]].add(word[i])
    return substitution


def intersect_substitutions(map_one, map_two, alphabet):
    """
    Поиск пересечения двух подстановок
    """
    intersected_subst = create_default_substitution(alphabet)
    for letter in intersected_subst.keys():
        suit_one = map_one[letter]
        suit_two = map_two[letter]
        if not suit_one or not suit_two:
            intersected_subst[letter] = suit_one | suit_two
        else:
            intersected_subst[letter] = suit_one & suit_two
    return intersected_subst


def remove_solved_letters(substitution):
    """
    Поиск подходящих букв
    """
    answer = copy(substitution)
    loop_again = True
    while loop_again:
        loop_again = False
        solved_letters = []
        for coded_letter in substitution.keys():
            potential_keys = answer[coded_letter]
            if len(answer[coded_letter]) == 1:
                solved_letters.append(list(potential_keys)[0])

        for coded_letter in substitution.keys():
            potential_keys = answer[coded_letter]
            for right_letter in solved_letters:
                if len(potential_keys) != 1 and right_letter in potential_keys:
                    potential_keys.remove(right_letter)
                    if len(potential_keys) == 1:
                        loop_again = True
    return answer


def replace_unrecognized_letters(substitution, alphabet):
    """
    Замена нерасшифрованных букв.
    """
    key = generate_substitution(alphabet)
    for coded_letter in substitution.keys():
        if len(substitution[coded_letter]) == 1:
            key[coded_letter] = list(substitution[coded_letter])[0]
        else:
            key[coded_letter] = '_'

    unrecognized = [letter for letter in key.keys()
                 if key[letter] == "_"]
    unused = [letter for letter in key.keys()
                      if letter not in key.values()]

    if len(unrecognized) == 1:
        key[unrecognized[0]] = unused[0]
    return key


def make_words_list(words, count=100):
    """
    Поиск популярных слов заданного количества
    """
    result = []
    sorted_groups = groupby(sorted(words.keys(), key=lambda x: (len(x), words[x]), reverse=True), lambda x: len(x))
    for _, group in sorted_groups:
        result.extend(list(group)[:count])
    return result


def load_stat(filename, encoding):
    """
    Парсинг JSON
    """
    with open(filename, "r", encoding=encoding) as file:
        sample = json.loads(file.read())
    return sample


class Decryptor:
    possible_keys = []

    def __init__(self, alphabet, stat_file, encoding, file_input=None, text_input=None, top=15000, benchmark=False):
        self.alphabet = alphabet
        self.file = file_input
        self.bench = benchmark
        self.encoding = encoding
        self.stat = load_stat(stat_file, encoding)
        self.word_patterns = get_wordlists_pattern(self.stat["words"].keys())
        if text_input:
            code_text_info = TextInfo(alphabet, encoding, input_text=text_input)
        elif file_input:
            code_text_info = TextInfo(alphabet, encoding, input_filename=file_input)
        else:
            raise Exception("Cipher's Text Input Error")
        self.cipher_words_list = code_text_info.find_info(top).make_count_dict()
        self.patterns = get_wordlists_pattern(make_words_list(self.cipher_words_list["words"], top))
        self.temp_subst = create_default_substitution(alphabet)
        self.key = create_default_substitution(alphabet)
        self.quadgrams = self.count_quadrams()

    def decrypt(self):
        global workdone
        i = 0
        for cipher_word in self.cipher_words_list["words"].keys():
            i +=1
            length = len(self.cipher_words_list["words"].keys())
            new_map = create_default_substitution(self.alphabet)
            pattern = get_pattern(cipher_word)
            if pattern not in self.patterns:
                continue
            if pattern in self.word_patterns.keys():
                for candidate in self.word_patterns[pattern]:
                    new_map = expand_substitution(new_map, cipher_word, candidate)
            self.temp_subst = intersect_substitutions(self.temp_subst, new_map, self.alphabet)
            if not self.bench:
                workdone = i / length
                print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(workdone * 50), workdone * 100), end="", flush=True)
                if workdone == 1:
                    workdone = 0
        result = remove_solved_letters(self.temp_subst)
        self.key = replace_unrecognized_letters(result, self.alphabet)
        return self.key

    def decode_file(self, file, encoding='utf-8', key=None):
        if not key:
            key = self.key
        return code_text_from_file(file, encoding, key)

    def decode_text(self, text, key=None):
        if not key:
            key = self.key
        return code(text, key)

    def count_substitutions_quality(self):
        """
        Подстановки, отсортированные (хорошая->плохая)
        """
        from math import factorial
        unrecognized = [letter for letter in self.key.keys() if self.key[
            letter] == "_"]
        used_substs = []
        result = {}
        max_score = -9999999999
        i = 0
        while i < 20:
            i += 1
            parent = self.create_random_with_unrecognized()
            decode = self.decode_text(self.file, parent)
            parent_score = self.count_precision_coefficient(decode)
            count = 0
            while count < 500:
                if len(used_substs) == factorial(len(unrecognized)):
                    break
                child = copy(parent)
                while child in used_substs or count == 0:
                    a = random.choice(unrecognized)
                    b = random.choice(unrecognized)
                    while a == b:
                        b = random.choice(unrecognized)
                    count += 1
                used_substs.append(child)
                child[a], child[b] = child[b], child[a]
                decode = self.decode_text(self.file, parent)
                child_score = self.count_precision_coefficient(decode)
                count += 1
                if child_score > parent_score:
                    parent_score = child_score
                    parent = copy(child)
                    count = 0
            if parent_score > max_score:
                max_score = parent_score
                result[max_score] = copy(parent)
        return OrderedDict(sorted(result.items(), reverse=True))

    def count_quadrams(self):
        from math import log10
        quadgrams = copy(self.stat['ngramms']['4'])
        n = sum(quadgrams.values())
        for key in quadgrams.keys():
            quadgrams[key] = log10(float(quadgrams[key]) / n)
        self.floor = log10(0.01 / n)
        return quadgrams

    def count_precision_coefficient(self, coded_text):
        score = 0
        coded_quadgrams = TextInfo(self.alphabet, self.encoding,
                                   input_text=coded_text).find_info(
            15000).make_ngramms_dict()['4']
        for quadgram in coded_quadgrams:
            if quadgram in self.quadgrams.keys():
                score += self.quadgrams[quadgram]
            else:
                score += self.floor
        return score

    def create_random_with_unrecognized(self):
        unused = [letter for letter in self.key.keys() if letter not
                          in self.key.values()]
        unrecognized = [letter for letter in self.key.keys() if self.key[
            letter] == "_"]
        subst = copy(self.key)
        for key in unrecognized:
            element = random.choice(unused)
            subst[key] = element
            unused.remove(element)
        return subst

