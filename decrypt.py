#!/usr/bin/env python3
# coding=utf-8
import argparse
import os
import sys
from logic.decryptor import Decryptor
call_picker = False

def main(stat, file, top, variants):
    global call_picker
    try:
        if stat is None:
            raise FileNotFoundError('Select file with statistics.')
        if file is None:
            raise FileNotFoundError('Select file with ecrypted text.')
    except FileNotFoundError as e:
        print(e)
        return e
    print('Stat file: {}\nEncrypted file: {}\nPopular words: {}\n'.format(stat, file, top))
    data = Decryptor('A-Za-z', stat, 'utf-8', file_input=file, top=top)
    key = data.decrypt()
    if "_" in key.values():
        key = choose_best_key(data, variants, file)
    decoded_text = data.decode_file(file, key)
    print(decoded_text)
    print('Substitution: {}'.format(key))


def choose_best_key(data, variants, file):
    global call_picker
    possibilities = list(data.count_substitutions_quality().values())[:variants]
    count = 0
    for subst in possibilities:
        print("Variant {}:".format(count))
        print(data.decode_file(file, 'utf-8', subst)[:300])
        print("========================")
        count += 1
    call_picker = True
    return possibilities[0]
    # return possibilities[int(input("Choose the better one:\n"))]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        usage='{} STAT FILE [TOP_WORDS] [VARIANTS]'.format(os.path.basename(sys.argv[0])),
        description='Decode text, encrypted in substitution cipher')

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
    parser.add_argument('-t', '--top', type=int, dest='top', default=15000,
                        help='choose, how many popular words will be stored')

    parser.add_argument('-v', '--variants', nargs='?', const=10,
                        dest='variants', type=int,
                        help='if the usual decryption process has left some '
                             'letters empty - try to guess them, '
                             'using another method, and then choose the best'
                             ' one')
    args = parser.parse_args()
    sys.exit(main(args.stat, args.file, args.top, args.variants))
