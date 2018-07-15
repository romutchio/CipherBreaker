#!/usr/bin/env python3
# coding=utf-8
import json
import re
import string
import sys
import tempfile
from collections import Counter, defaultdict

LETTERS = "letters"
WORDS = "words"
NGRAMMS = "ngramms"


class CountInfo:
    def __init__(self, letters, words, ngramms):
        self.letters = letters
        self.words = words
        self.ngramms = ngramms

    def make_ngramms_dict(self):
        return {str(n): dict(self.ngramms[str(n)]) for n in self.ngramms}

    def make_count_dict(self):
        """
        Создание словаря с информацией, сколько букв появилось в тексте
        и самые популярные
        """
        return {LETTERS: dict(self.letters),
                WORDS: dict(self.words),
                NGRAMMS: self.make_ngramms_dict()}

    def make_frequency_dict(self):
        """
        Словарь частот
        """
        return {LETTERS: count_frequencies(dict(self.letters)),
                WORDS: count_frequencies(dict(self.words))}

    def update_count_info(self, filename, alphabet, top_words, encoding):
        """
        Обновление информации из файла
        """
        try:
            with open(filename, "r", encoding=encoding) as f:
                prev_data = json.loads(f.read())
            if alphabet.match(list(prev_data[LETTERS].keys())[0]) is None:
                return
            else:
                self.letters += Counter(prev_data[LETTERS])
                self.words += Counter(prev_data[WORDS])
                old_ngramms = {}
                for n in prev_data[NGRAMMS]:
                    old_ngramms[n] = Counter(prev_data[NGRAMMS][n])
                for n in old_ngramms:
                    self.ngramms[n] += old_ngramms[n]

            if len(self.words) > top_words:
                self.words = Counter(dict(self.words.most_common(top_words)))
            return
        except FileNotFoundError:
            return


class TextInfo:
    """
    Информация о текущем тексте
    """

    def __init__(self, alphabet, encoding, input_filename=None, input_text=None):
        self.input = input_filename
        self.alph = re.compile('[' + alphabet + ']')
        self.letters = Counter()
        self.words = Counter()
        self.ngramms = defaultdict(Counter)
        self.encoding = encoding
        self.text = input_text

    def find_info(self, top_words):
        """
        Функция подсчитывает буквы в файле и слова в тексте
        """
        if top_words is None:
            top_words = 100
        if self.text is not None:
            leftover = self.__count(self.text)
        else:
            with open(self.input, "rb") as f:
                leftover = self.__count(f.read().decode('utf-8'))

        if leftover != '':
            self.words[leftover] += 1
            self.make_ngramms(leftover)

        if len(self.words) > top_words:
            self.words = Counter(dict(self.words.most_common(top_words)))

        return CountInfo(self.letters, self.words, self.ngramms)

    def make_ngramms(self, word):
        for n in range(2, len(word) + 1):
            ngramms = word_to_ngramms(word, n)
            for ngramm in ngramms:
                self.ngramms[str(n)][ngramm] += 1

    def __count(self, text):
        word = ''
        for line in text:
            for char in line:
                if self.alph.match(char) is not None:
                    word += char.lower()
                    self.letters[char.lower()] += 1
                if char in string.whitespace or char in string.punctuation \
                        or char == '—':
                    if word != '':
                        self.words[word] += 1
                        self.make_ngramms(word)
                    word = ''
        return word


def word_to_ngramms(text, n):
    """ Конвертер текста в нграммы """
    return [text[i:i + n] for i in range(len(text) - n + 1)]


def count_frequencies(dictionary):
    divider = sum(dictionary.values())
    return {k: v / divider for k, v in dictionary.items()}


def write_json_in_file(filename, data, encoding):
    with open(filename, "w", encoding=encoding) as f:
        f.write(json.dumps(data))
