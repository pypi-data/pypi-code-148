__author__ = "Nishat, DevStrikerTech"
__status__ = "planning"

import os
import glob
from itertools import takewhile, repeat, islice


def split_file(src_type, file_split_by_lines_or_size, file_path):
    if src_type == 'split':
        for filename in glob.iglob('{}/**'.format(file_path), recursive=True):
            if os.path.isfile(filename):
                # Separate file name and extension
                file_title = os.path.splitext(os.path.basename(filename))[0]
                file_extension = os.path.splitext(os.path.basename(filename))[1]

                if not file_split_by_lines_or_size.endswith('gb'):
                    # Get total number of lines from source file
                    input_file = open(filename, 'rb')
                    read_lines = takewhile(lambda line: line, (input_file.raw.read(1024 * 1024) for _ in repeat(None)))
                    total_lines = sum(each_line.count(b'\n') for each_line in read_lines)

                    if total_lines > int(file_split_by_lines_or_size):
                        # Create directory as same source directory
                        source_file_name = filename.split('/')[-2]
                        os.mkdir('target/{}'.format(source_file_name))

                        """
                        Split files into multiples based on line numbers
                        """
                        with open(filename) as target_file:
                            for index, lines in enumerate(iter(lambda: list(islice(target_file,
                                                                                   int(file_split_by_lines_or_size))),
                                                               []),
                                                          1):
                                with open(
                                        'target/{}/{}_{}{}'.format(source_file_name, file_title, index, file_extension),
                                        'w') as write_to_target:
                                    write_to_target.writelines(lines)
