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
from proquo.core.ProQuo import ProQuo
from proquo.model.reference.ReferenceModel import ReferenceModel
from proquo.model.relation.RelationVectorizerBert import RelationVectorizerBert
import transformers

from proquo.model.reference.ReferenceVectorizer import ReferenceVectorizer
from proquo.testing.reference import TestReference
from proquo.testing.relation import TestRelationBert, TestRelationLstm
from proquo.training.reference import TrainReference
from proquo.training.relation import TrainRelationBert

# only import if tensorflow_text is found. This is hardly ever needed and tensorflow_text is not always easy to install.
try:
    from proquo.training.relation import TrainRelationLstm
except ModuleNotFoundError:
    pass


def __process_file(pro_quo, filename, source_file_content, target_file_content, quid_matches, output_folder_path,
                   source_text_parallel_print):

    short_matches: List[MatchRef] = pro_quo.compare(source_file_content, target_file_content, quid_matches,
                                                    source_text_parallel_print)

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


def __train_reference(train_file_path, val_file_path, output_path):
    TrainReference.train(train_file_path, val_file_path, output_path)


def __train_relation(train_file_path, val_file_path, output_path, arch_type):
    if arch_type == 'bert':
        TrainRelationBert.train(train_file_path, val_file_path, output_path)
    elif arch_type == 'lstm':
        TrainRelationLstm.train(train_file_path, val_file_path, output_path)


def __test_reference(test_file_path, vocab_file_path, model_file_path):
    TestReference.test(test_file_path, vocab_file_path, model_file_path)


def __test_relation_lstm(test_file_path, vocab_file_path, model_file_path):
    TestRelationLstm.test(test_file_path, vocab_file_path, model_file_path)


def __test_relation_bert(test_file_path, tokenizer_folder_path, model_folder_path):
    TestRelationBert.test(test_file_path, tokenizer_folder_path, model_folder_path)


def __run_compare(source_file_path, target_path, ref_vocab_file_path, ref_model_file_path, rel_tokenizer_folder_path,
                  rel_model_folder_path, quid_match_path, output_folder_path, parallel_print_files):

    reference_vectorizer = ReferenceVectorizer.from_vocab_file(ref_vocab_file_path, 25, True)
    reference_model = ReferenceModel(25, True, 32, 32, 0.2, 512, 10)
    reference_keras_model = reference_model.get_model(reference_vectorizer.max_id)
    reference_keras_model.load_weights(ref_model_file_path)

    relation_vectorizer = RelationVectorizerBert.from_saved(300, rel_tokenizer_folder_path, True)
    relation_model = transformers.TFBertForSequenceClassification.from_pretrained(rel_model_folder_path, num_labels=2)

    with open(source_file_path, 'r', encoding='utf-8') as source_file:
        source_file_content = source_file.read().lower()

    pro_quo = ProQuo(reference_keras_model, reference_vectorizer, relation_model, relation_vectorizer)

    if isfile(target_path) and target_path.endswith('.txt'):
        with open(target_path, 'r', encoding='utf-8') as target_file:
            target_file_content = target_file.read()

        filename = splitext(basename(target_path))[0]

        if quid_match_path:
            quid_matches = load_matches(quid_match_path)
        else:
            quid = Quid(min_match_length=2, keep_ambiguous_matches=True)
            quid_matches = quid.compare(source_file_content, target_file_content)

        source_text_parallel_print = False

        if filename in parallel_print_files:
            source_text_parallel_print = True

        __process_file(pro_quo, filename, source_file_content, target_file_content, quid_matches, output_folder_path,
                       source_text_parallel_print)
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

                source_text_parallel_print = False

                if filename in parallel_print_files:
                    source_text_parallel_print = True

                __process_file(pro_quo, filename, source_file_content, target_file_content, quid_matches,
                               output_folder_path, source_text_parallel_print)


def main(argv=None):
    train_description = 'TBD'
    train_reference_description = 'TBD'
    train_relation_description = 'TBD'
    test_description = 'TBD'
    test_reference_description = 'TBD'
    test_relation_description = 'TBD'

    compare_description = 'TBD'

    argument_parser = ArgumentParser(description='ProQuo is a tool to find (short) quotations in texts.')

    subparsers_command = argument_parser.add_subparsers(dest='command')
    subparsers_command.required = True

    parser_train = subparsers_command.add_parser('train', help=train_description, description=train_description)
    subparsers_train_model = parser_train.add_subparsers(dest='train_model')
    subparsers_train_model.required = True

    parser_train_reference = subparsers_train_model.add_parser('reference', help=train_reference_description,
                                                               description=train_reference_description)

    parser_train_reference.add_argument('train_file_path', nargs=1, metavar='train-file-path',
                                        help='Path to the txt file containing the training examples')
    parser_train_reference.add_argument('val_file_path', nargs=1, metavar='val-file-path',
                                        help='Path to the txt file containing the validation examples')
    parser_train_reference.add_argument('output_folder_path', nargs=1, metavar='output-folder_path',
                                        help='Path to the folder for storing the output model and vocabulary')
    parser_train_reference.add_argument('--create-dated-subfolder', dest='create_dated_subfolder', default=False,
                                        action='store_true',
                                        help='Create a subfolder named with the current date to store the results')
    parser_train_reference.add_argument('--no-create-dated-subfolder', dest='create_dated_subfolder',
                                        action='store_false',
                                        help='Do not create a subfolder named with the current date to store the '
                                             'results')

    parser_train_relation = subparsers_train_model.add_parser('relation', help=train_relation_description,
                                                              description=train_relation_description)

    parser_train_relation.add_argument('train_file_path', nargs=1, metavar='train-file-path',
                                       help='Path to the txt file containing the training examples')
    parser_train_relation.add_argument('val_file_path', nargs=1, metavar='val-file-path',
                                       help='Path to the txt file containing the validation examples')
    parser_train_relation.add_argument('output_folder_path', nargs=1, metavar='output-folder-path',
                                       help='Path to the folder for storing the output model and vocabulary')
    parser_train_relation.add_argument('--create-dated-subfolder', dest='create_dated_subfolder', default=False,
                                       action='store_true',
                                       help='Create a subfolder named with the current date to store the results')
    parser_train_relation.add_argument('--no-create-dated-subfolder', dest='create_dated_subfolder',
                                       action='store_false',
                                       help='Do not create a subfolder named with the current date to store the results')
    parser_train_relation.add_argument('--arch', choices=['lstm', 'bert'], dest='arch_type', default='bert',
                                       help='The model architecture to train')

    parser_test = subparsers_command.add_parser('test', help=test_description, description=test_description)
    subparsers_test_model = parser_test.add_subparsers(dest='test_model')
    subparsers_test_model.required = True

    parser_test_reference = subparsers_test_model.add_parser('reference', help=test_reference_description,
                                                             description=test_reference_description)

    parser_test_reference.add_argument('test_file_path', nargs=1, metavar='test-file-path',
                                       help='Path to the txt file containing the testing examples')
    parser_test_reference.add_argument('vocab_file_path', nargs=1, metavar='vocab-file-path',
                                       help='Path to the vocab file')
    parser_test_reference.add_argument('model_file_path', nargs=1, metavar='model-file-path',
                                       help='Path to the model file')

    parser_test_relation = subparsers_test_model.add_parser('relation', help=test_relation_description,
                                                            description=test_relation_description)

    subparsers_test_relation_arch = parser_test_relation.add_subparsers(dest='test_model_relation_arch')
    subparsers_test_relation_arch.required = True

    parser_test_relation_lstm = subparsers_test_relation_arch.add_parser('lstm', help='',
                                                                         description='')

    parser_test_relation_lstm.add_argument('test_file_path', nargs=1, metavar='test-file-path',
                                           help='Path to the txt file containing the testing examples')
    parser_test_relation_lstm.add_argument('vocab_file_path', nargs=1, metavar='vocab-file-path',
                                           help='Path to the vocab file')
    parser_test_relation_lstm.add_argument('model_file_path', nargs=1, metavar='model-file-path',
                                           help='Path to the model file')

    parser_test_relation_bert = subparsers_test_relation_arch.add_parser('bert', help='',
                                                                         description='')

    parser_test_relation_bert.add_argument('test_file_path', nargs=1, metavar='test-file-path',
                                           help='Path to the txt file containing the testing examples')
    parser_test_relation_bert.add_argument('tokenizer_folder_path', nargs=1, metavar='tokenizer-folder-path',
                                           help='Path to the vocab file')
    parser_test_relation_bert.add_argument('model_folder_path', nargs=1, metavar='model-folder-path',
                                           help='Path to the model file')

    parser_compare = subparsers_command.add_parser('compare', help=compare_description, description=compare_description)

    parser_compare.add_argument('source_file_path', nargs=1, metavar='source-file-path',
                                help='Path to the source text file')
    parser_compare.add_argument('target_path', nargs=1, metavar='target-path',
                                help='Path to the target text file or folder')
    parser_compare.add_argument('ref_vocab_file_path', nargs=1, metavar='ref-vocab-file-path',
                                help='Path to the reference vocab text file')
    parser_compare.add_argument('ref_model_file_path', nargs=1, metavar='ref-model-file-path',
                                help='Path to the reference model file')
    parser_compare.add_argument('rel_tokenizer_folder_path', nargs=1, metavar='rel-tokenizer-folder-path',
                                help='Path to the relation tokenizer folder')
    parser_compare.add_argument('rel_model_folder_path', nargs=1, metavar='rel-model-folder-path',
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
    parser_compare.add_argument('--parallel-print-files', dest='parallel_print_files', nargs='*')

    args = argument_parser.parse_args(argv)

    if args.command == 'train':
        if args.train_model == 'reference':
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

            __train_reference(train_file_path, val_file_path, output_folder_path)

        elif args.train_step == 'relation':
            train_file_path = args.train_file_path[0]
            val_file_path = args.val_file_path[0]
            output_folder_path = args.output_folder_path[0]
            create_dated_subfolder = args.create_dated_subfolder
            arch_type = args.arch_type

            if create_dated_subfolder:
                now = datetime.now()
                date_time_string = now.strftime('%Y_%m_%d_%H_%M_%S')
                output_folder_path = join(output_folder_path, date_time_string)
                Path(output_folder_path).mkdir(parents=True, exist_ok=True)

            __train_relation(train_file_path, val_file_path, output_folder_path, arch_type)

    elif args.command == 'test':
        if args.test_model == 'reference':
            test_file_path = args.test_file_path[0]
            vocab_file_path = args.vocab_file_path[0]
            model_file_path = args.model_file_path[0]
            __test_reference(test_file_path, vocab_file_path, model_file_path)

        elif args.test_model == 'relation':
            if args.test_model_relation_arch == 'lstm':
                test_file_path = args.test_file_path[0]
                vocab_file_path = args.vocab_file_path[0]
                model_file_path = args.model_file_path[0]
                __test_relation_lstm(test_file_path, vocab_file_path, model_file_path)

            elif args.test_model_relation_arch == 'bert':
                test_file_path = args.test_file_path[0]
                tokenizer_folder_path = args.tokenizer_folder_path[0]
                model_folder_path = args.model_folder_path[0]
                __test_relation_bert(test_file_path, tokenizer_folder_path, model_folder_path)

    elif args.command == 'compare':
        source_file_path = args.source_file_path[0]
        target_path = args.target_path[0]
        ref_vocab_file_path = args.ref_vocab_file_path[0]
        ref_model_file_path = args.ref_model_file_path[0]
        rel_tokenizer_folder_path = args.rel_tokenizer_folder_path[0]
        rel_model_folder_path = args.rel_model_folder_path[0]
        quid_match_path = args.quid_match_path
        output_folder_path = args.output_folder_path
        create_dated_subfolder = args.create_dated_subfolder
        parallel_print_files = args.parallel_print_files

        if create_dated_subfolder:
            now = datetime.now()
            date_time_string = now.strftime('%Y_%m_%d_%H_%M_%S')
            output_folder_path = join(output_folder_path, date_time_string)
            Path(output_folder_path).mkdir(parents=True, exist_ok=True)

        __run_compare(source_file_path, target_path, ref_vocab_file_path, ref_model_file_path,
                      rel_tokenizer_folder_path, rel_model_folder_path, quid_match_path, output_folder_path,
                      parallel_print_files)


if __name__ == '__main__':
    sys.exit(main())
