#!/usr/bin/env python3
# coding=utf-8
import argparse
import os
import sys
from logic.learner import write_json_in_file
from logic.encryptor import read_json_file, \
    generate_substitution, code_text_from_file


def main(file, substitution=None, save=None, output=None):
    try:
        if file is None:
            raise FileNotFoundError('Select file for encrypt.')
    except FileNotFoundError as e:
        print(e)
        return e

    if substitution:
        subst = read_json_file(substitution, 'utf-8')
    else:
        subst = generate_substitution('A-Za-z')
    if not file:
        result = code_stdin(subst)
    else:
        result = code_text_from_file(file, 'utf-8', subst)

    if save:
        write_json_in_file('substitution.txt', subst, 'utf-8')

    if output:
        with open(output, 'w', encoding='utf-8') as file:
            file.write(result)
    else:
        sys.stdout.write(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='{} File [SUBSTITUTION]'.format(os.path.basename(sys.argv[0])),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='Encode text using substitution cipher')
    parser.add_argument(
        'file',
        metavar='FILE',
        nargs='?',
        default=None,
        help='name of file for encrypting')
    parser.add_argument(
        '-s',
        '--substitution',
        type=str,
        dest='substitution',
        metavar="SUBST",
        help='name of file with substituion')

    args = parser.parse_args()
    subst = args.substitution

    sys.exit(main(args.file, substitution=subst, save=True, output='crypto.txt'))
