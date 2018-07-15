#!/usr/bin/env python3
# coding=utf-8
import argparse
import os
import sys
from pprint import pprint
from logic.learner import TextInfo, write_json_in_file

LETTERS = "letters"
WORDS = "words"
NGRAMMS = "ngramms"
workdone = 0


def main(files=None, top=15000, update_file=None):
    try:
        if files is None:
            raise FileNotFoundError('Select file/files for learning.')
    except FileNotFoundError as e:
        print(e)
        return e

    if len(files) > 1:
        learn_multiple_files(top, files, update_file=update_file)
    else:
        learn_single_file(top, file_name=files[0], update_file=update_file)

def get_progress():
    return workdone

def learn_multiple_files(top, files, update_file=None):
    global workdone
    print('Learning multiple files: {}'.format(len(files)))
    for i in range(0, len(files)):
        text_info = TextInfo('A-Za-z', 'utf-8', input_filename=files[i])
        count_info = text_info.find_info(top)
        if update_file is not None:
            count_info.update_count_info(
                update_file,
                text_info.alph,
                top,
                'utf-8')
            updated_dict = count_info.make_count_dict()
        else:
            updated_dict = count_info.make_count_dict()
        write_json_in_file('result.txt', updated_dict, 'utf-8')
        workdone = (i+1) / (len(files))
        print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(workdone * 50), workdone * 100), end="", flush=True)
        if workdone == 1:
            workdone = 0

def learn_single_file(top, update_file = None, file_name=None):
    print('Learning single file')
    if file_name:
        text_info = TextInfo(
            'A-Za-z',
            'utf-8',
            input_filename=file_name)
    count_info = text_info.find_info(top)
    if update_file is not None:
        count_info.update_count_info(
            update_file,
            text_info.alph,
            top,
            'utf-8')
        updated_dict = count_info.make_count_dict()
    else:
        updated_dict = count_info.make_count_dict()
    write_json_in_file('result.txt', updated_dict, 'utf-8')
    print('Done')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='{} [OPTIONS] ALPHABET FILE'.format(
        os.path.basename(sys.argv[0])), description='Learn letter frequency')
    parser.add_argument(
        'file',
        metavar='FILE',
        nargs='*',
        default=None,
        help="File or files via ','")
    parser.add_argument('-t', '--top', type=int, dest='top', default=15000,
                        help='choose, how many popular words will be stored')
    parser.add_argument(
        '-u',
        '--update',
        type=str,
        dest='update',
        metavar="FILENAME",
        help='choose, which file is to be updated')

    args = parser.parse_args()
    if args.file:
        files = args.file[0].split(',')
        sys.exit(main(files, args.top, args.update))
