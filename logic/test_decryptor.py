#!/usr/bin/env python3
import tempfile
import unittest
import logic.decryptor as decryptor
import json

ENCODING = "utf-8"


class MyTestCase(unittest.TestCase):
    def test_make_mask(self):
        word_one = "hello"
        mask_one = "01223"
        word_two = "puppy"
        mask_two = "01002"
        self.assertEqual(mask_one, decryptor.get_pattern(word_one))
        self.assertEqual(mask_two, decryptor.get_pattern(word_two))

    def test_make_words_masks(self):
        self.assertEqual(decryptor.get_wordlists_pattern(
            ["lazy", 'summer', "abcdef", "qwerty"]),
            {"0123": ["lazy"],
             "012234": ["summer"],
             "012345": ["abcdef", "qwerty"]})

    def test_get_blank_letter_mapping(self):
        self.assertDictEqual(decryptor.create_default_substitution("A-Za-z"),
                             make_dict_of_smth(make_alphabet_keys("A-Za-z"),
                                               set()))

    def test_intersect(self):
        subst_one = make_dict_of_smth(make_alphabet_keys("A-Za-z"), set())
        subst_one['a'] = {'b', 'c'}
        subst_one['b'] = {'a'}
        subst_one['d'] = {'x'}
        subst_two = make_dict_of_smth(make_alphabet_keys("A-Za-z"), set())
        subst_two['a'] = {'c', 'd'}
        subst_two['b'] = {'e'}
        subst_two['c'] = {'z'}
        expected_result = make_dict_of_smth(make_alphabet_keys("A-Za-z"),
                                            set())
        expected_result['a'] = {'c'}
        expected_result['c'] = {'z'}
        expected_result['d'] = {'x'}
        self.assertDictEqual(
            expected_result,
            decryptor.intersect_substitutions(
                subst_one,
                subst_two,
                "A-Za-z"))

    def test_remove_solved_letters(self):
        subst_one = make_dict_of_smth(make_alphabet_keys("A-Za-z"), set())
        subst_one['a'] = {'a', 'b'}
        subst_one['b'] = {'a'}
        subst_one['d'] = {'x'}

        expected_result = make_dict_of_smth(make_alphabet_keys("A-Za-z"),
                                            set())
        expected_result['a'] = {'b'}
        expected_result['b'] = {'a'}
        expected_result['d'] = {'x'}
        self.assertDictEqual(
            expected_result,
            decryptor.remove_solved_letters(subst_one))

    def test_find_final(self):
        subst = make_dict_of_smth(make_alphabet_keys("A-Za-z"), set())
        subst['a'] = {'c', 'd'}
        subst['b'] = {'e'}
        subst['c'] = {'z'}
        expected_result = make_dict_of_smth(make_alphabet_keys("A-Za-z"), "_")
        expected_result['b'] = 'e'
        expected_result['c'] = 'z'
        self.assertDictEqual(
            expected_result,
            decryptor.replace_unrecognized_letters(
                subst,
                "A-Za-z"))

    def test_make_words_list(self):
        words = {
            "the": 900,
            "and": 2,
            "to": 45,
            "he": 12,
            "a": 9,
            "harry": 1327,
            "of": 9000000,
            "it": 900,
            "was": 4567,
            "you": 1037,
            "s": 1019,
        }
        expected_result = ["harry", "was", "of", "s"]
        self.assertEqual(expected_result, decryptor.make_words_list(words, 1))

    def test_expand_substitution(self):
        word = "abc"
        coded = "xyz"
        subst = make_dict_of_smth(make_alphabet_keys("A-Za-z"), set())
        subst['x'] = {'a'}
        subst['y'] = {'b'}
        subst['z'] = {'c'}
        self.assertDictEqual(subst, decryptor.expand_substitution(
            decryptor.create_default_substitution("A-Za-z"), coded, word))

    def test_process_stat(self):
        stat = """"{"words": {"hello": 1, "my": 1, "friend": 1, "no": 1}}"""
        with open('json.txt', "w") as file:
            return file.write(stat)
        processed = decryptor.load_statistic('json.txt', 'utf-8')
        expected = {"words": {"hello": 1, "my": 1, "friend": 1, "no": 1}}
        self.assertDictEqual(expected, processed)


def make_alphabet_keys(alphabet):
    return decryptor.create_default_substitution(alphabet).keys()


def make_dict_of_smth(keys, smth):
    return {key: smth for key in keys}





if __name__ == '__main__':
    unittest.main()
