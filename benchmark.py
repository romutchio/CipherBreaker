# coding=utf-8
# !/usr/bin/env python3
# coding=utf-8
import argparse
import os
import sys
from pprint import pprint
from logic.learner import write_json_in_file
from logic.decryptor import Decryptor
import logic.encryptor as encryptor
import matplotlib.pyplot as plt

workdone =0


def main(stat, filename, iterations, top, debug):
    global workdone
    if stat is None:
        raise FileNotFoundError('Select file with statistics.')
    if filename is None:
        raise FileNotFoundError('Select file with ecrypted text.')
    if iterations is None:
        raise Exception('Iterations')

    print('Stat file: {}\nEncrypted file: {}\nIterations: {}\nPopular words: {}\n'.format(stat, filename, iterations, top))
    with open(filename, 'rb') as file:
        original_text = file.read().decode('utf-8')
    coded_text = encryptor.code(original_text, encryptor.generate_substitution('A-Za-z'))

    result = {}
    for n in range(1, iterations+1):
        sample = coded_text[:n * 50]
        original_sample = original_text[:n * 50]
        data = Decryptor('A-Za-z', stat, 'utf-8', text_input=sample, top=top, benchmark=True)
        data.decrypt()
        decoded_sample = data.decode_text(sample)
        diff = count_diff(decoded_sample, original_sample)
        res = ((len(sample) - diff) * 100) / len(sample)
        result[n * 50] = res
        if debug:
            print("\rTotal text's length: {}, Piece's length: {}, Iteration: {}, Recognized: {}%;\n"
                  .format(str(len(coded_text)), str(n * 25), str(n), str(round(res, 2))), end="", flush=True)
        if len(coded_text) < n * 50:
            break
        workdone = n /(iterations)
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(workdone * 50), workdone * 100), end="", flush=True)
        if workdone == 1:
            workdone = 0
    print(decoded_sample)
    plt.figure()
    plt.plot(list(result.keys()), list(result.values()))
    plt.xlabel("Text's length")
    plt.ylabel("Success rate, %")
    plt.title("Benchmark")
    plt.grid(True)
    plt.savefig("benchmark.png")
    coords = list(result.keys()), list(result.values())
    return coords


def count_diff(text_one, text_two):
    """
    Кол-во различных символов в двух текстах
    """
    return len([x for x in zip(text_one, text_two) if x[0] != x[1]])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='{} [OPTIONS] STAT FILE'.format(
            os.path.basename(sys.argv[0])),
        description='count the percentage of correctly guessed letters')

    parser.add_argument(
        'stat',
        metavar='stat',
        help='statistics of the language')

    parser.add_argument(
        'file',
        metavar='FILE',
        nargs='?',
        default=sys.stdin,
        help='name of the file with text')
    parser.add_argument(
        '-i',
        '--iter',
        type=int,
        dest='iter',
        default=51,
        help='choose a quantity of iterations')

    parser.add_argument('-t', '--top', type=int, dest='top', default=15000,
                        help='choose, how many popular words will be stored')
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        dest='debug',
        help='enable debug output')
    args = parser.parse_args()
    main(args.stat, args.file, args.iter, args.top, args.debug)
    sys.exit()
