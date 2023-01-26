from argparse import ArgumentParser
import sys

from os.path import join, isfile, splitext, basename, isdir, exists
from os import listdir
from datetime import datetime
from pathlib import Path
from typing import List

from quid.core.Quid import Quid
from quid.helper.Loader import load_matches

from proquo.core.MatchRef import MatchRef
from proquo.core.ProQuoLm import ProQuoLm
from proquo.model.linking.LinkingVectorizer import LinkingVectorizer
import transformers

from proquo.testing.linking import TestLinking
from proquo.training.linking import TrainLinking


def __process_file(pro_quo_lm, filename, source_file_content, target_file_content, quid_matches, output_folder_path):
    short_matches: List[MatchRef] = pro_quo_lm.compare(source_file_content, target_file_content, quid_matches)

    # todo: an Quid anpassen
    result = ''

    for match in short_matches:
        result += f'\n{match.source_span.start}\t{match.source_span.end}' \
                  f'\t{match.target_span.start}\t{match.target_span.end}' \
                  f'\t{match.source_span.text}\t{match.target_span.text}'

        if match.reference:
            result += f'\t{match.reference.start}\t{match.reference.end}\t{match.reference.text}'

    if output_folder_path:
        with open(join(output_folder_path, filename + '.csv'), 'w', encoding='utf-8') as output_file:
            output_file.write(result)
    else:
        print('Results:')
        print(result)


def __train(train_file_path, val_file_path, output_path):
    TrainLinking.train(train_file_path, val_file_path, output_path)


def __test(test_file_path, tokenizer_folder_path, model_folder_path):
    TestLinking.test(test_file_path, tokenizer_folder_path, model_folder_path)


def __run_compare(source_file_path, target_path, tokenizer_folder_path, model_folder_path, quid_match_path,
                  output_folder_path):

    link_vectorizer = LinkingVectorizer.from_saved(512, tokenizer_folder_path, True)
    link_model = transformers.TFBertForSequenceClassification.from_pretrained(model_folder_path, num_labels=2)

    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        source_file_content = source_file.read().lower()

    pro_quo_lm = ProQuoLm(link_model, link_vectorizer)

    if isfile(target_path) and target_path.endswith('.txt'):
        with open(target_path, 'r', encoding='utf-8') as target_file:
            target_file_content = target_file.read()

        filename = splitext(basename(target_path))[0]

        if quid_match_path:
            quid_matches = load_matches(quid_match_path)
        else:
            quid = Quid(min_match_length=2, keep_ambiguous_matches=True)
            quid_matches = quid.compare(source_file_content, target_file_content)

        __process_file(pro_quo_lm, filename, source_file_content, target_file_content, quid_matches, output_folder_path)
    elif isdir(target_path):
        for fileOrFolder in listdir(target_path):
            target_file_path = join(target_path, fileOrFolder)

            if isfile(target_file_path) and target_file_path.endswith('.txt'):
                filename = splitext(basename(target_file_path))[0]

                with open(target_file_path, 'r', encoding='utf-8') as target_file:
                    target_file_content = target_file.read()

                if quid_match_path:
                    match_file_path = join(quid_match_path, filename + '.json')
                    quid_matches = load_matches(match_file_path)
                else:
                    quid = Quid(min_match_length=2, keep_ambiguous_matches=True)
                    quid_matches = quid.compare(source_file_content, target_file_content)

                __process_file(pro_quo_lm, filename, source_file_content, target_file_content, quid_matches,
                               output_folder_path)


def main(argv=None):
    train_description = 'TBD'
    train_linking_description = 'TBD'
    test_description = 'TBD'
    test_linking_description = 'TBD'

    compare_description = 'TBD'

    argument_parser = ArgumentParser(description='ProQuoLm is a tool to find (short) quotations in texts.')

    subparsers_command = argument_parser.add_subparsers(dest='command')
    subparsers_command.required = True

    parser_train = subparsers_command.add_parser('train', help=train_description, description=train_description)

    parser_train.add_argument('train_file_path', nargs=1, metavar='train-file-path',
                              help='Path to the txt file containing the training examples')
    parser_train.add_argument('val_file_path', nargs=1, metavar='val-file-path',
                              help='Path to the txt file containing the validation examples')
    parser_train.add_argument('output_folder_path', nargs=1, metavar='output-folder_path',
                              help='Path to the folder for storing the output model and vocabulary')
    parser_train.add_argument('--create-dated-subfolder', dest='create_dated_subfolder', default=False,
                              action='store_true',
                              help='Create a subfolder named with the current date to store the results')
    parser_train.add_argument('--no-create-dated-subfolder', dest='create_dated_subfolder',
                              action='store_false',
                              help='Do not create a subfolder named with the current date to store the '
                                   'results')

    parser_test = subparsers_command.add_parser('test', help=test_description, description=test_description)

    parser_test.add_argument('test_file_path', nargs=1, metavar='test-file-path',
                             help='Path to the txt file containing the testing examples')
    parser_test.add_argument('tokenizer_folder_path', nargs=1, metavar='tokenizer-folder-path',
                             help='Path to the vocab file')
    parser_test.add_argument('model_folder_path', nargs=1, metavar='model-folder-path',
                             help='Path to the model file')

    parser_compare = subparsers_command.add_parser('compare', help=compare_description, description=compare_description)

    parser_compare.add_argument('source_file_path', nargs=1, metavar='source-file-path',
                                help='Path to the source text file')
    parser_compare.add_argument('target_path', nargs=1, metavar='target-path',
                                help='Path to the target text file or folder')
    parser_compare.add_argument('tokenizer_folder_path', nargs=1, metavar='tokenizer-folder-path',
                                help='Path to the relation tokenizer folder')
    parser_compare.add_argument('model_folder_path', nargs=1, metavar='model-folder-path',
                                help='Path to the relation model folder')
    parser_compare.add_argument('--quid-match-path', dest='quid_match_path',
                                help='Path to the file or folder with quid matches. If this option is not set, then'
                                     ' Quid is used to find long matches.')
    parser_compare.add_argument('--output-folder-path', dest='output_folder_path',
                                help='The output folder path. If this option is set the output will be saved to a file'
                                     ' created in the specified folder')
    parser_compare.add_argument('--create-dated-subfolder', dest='create_dated_subfolder', default=False,
                                action='store_true',
                                help='Create a subfolder named with the current date to store the results')
    parser_compare.add_argument('--no-create-dated-subfolder', dest='create_dated_subfolder',
                                action='store_false',
                                help='Do not create a subfolder named with the current date to store the results')

    args = argument_parser.parse_args(argv)

    if args.command == 'train':
        train_file_path = args.train_file_path[0]
        val_file_path = args.val_file_path[0]
        output_folder_path = args.output_folder_path[0]
        create_dated_subfolder = args.create_dated_subfolder

        if output_folder_path:
            if not exists(output_folder_path):
                raise Exception(f'{output_folder_path} does not exist!')

        if create_dated_subfolder:
            now = datetime.now()
            date_time_string = now.strftime('%Y_%m_%d_%H_%M_%S')
            output_folder_path = join(output_folder_path, date_time_string)
            Path(output_folder_path).mkdir(parents=True, exist_ok=True)

        __train(train_file_path, val_file_path, output_folder_path)

    elif args.command == 'test':
        test_file_path = args.test_file_path[0]
        tokenizer_folder_path = args.tokenizer_folder_path[0]
        model_folder_path = args.model_folder_path[0]
        __test(test_file_path, tokenizer_folder_path, model_folder_path)

    elif args.command == 'compare':
        source_file_path = args.source_file_path[0]
        target_path = args.target_path[0]
        tokenizer_folder_path = args.tokenizer_folder_path[0]
        model_folder_path = args.model_folder_path[0]
        quid_match_path = args.quid_match_path
        output_folder_path = args.output_folder_path
        create_dated_subfolder = args.create_dated_subfolder

        if create_dated_subfolder:
            now = datetime.now()
            date_time_string = now.strftime('%Y_%m_%d_%H_%M_%S')
            output_folder_path = join(output_folder_path, date_time_string)
            Path(output_folder_path).mkdir(parents=True, exist_ok=True)

        __run_compare(source_file_path, target_path, tokenizer_folder_path, model_folder_path, quid_match_path,
                      output_folder_path)


if __name__ == '__main__':
    sys.exit(main())
