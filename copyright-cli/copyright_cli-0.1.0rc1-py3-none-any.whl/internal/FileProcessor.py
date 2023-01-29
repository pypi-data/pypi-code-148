from .CopyrightInfo import CopyrightInfo
from enum import Enum
import os


class _SearchState(Enum):
    SEARCHING_FOR_PREFIX = 0
    SEARCHING_FOR_SUFFIX = 1
    KEEP_REMAINING = 2


def has_copyright(input_path, copyright_info: CopyrightInfo):
    with open(input_path, 'rt') as file:
        return copyright_info.full_text in file.read()


def add_copyright_to_file(input_path, output_path, copyright_info: CopyrightInfo):
    with open(input_path, 'rt') as file:
        file_contents = file.read()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w+t') as file:
        file.write(f"{copyright_info.full_text}{file_contents}")


def remove_copyright_from_file(input_path, output_path, copyright_info: CopyrightInfo):
    with open(input_path, 'rt') as file:
        contents = file.readlines()

    updated_contents = _remove_copyright(contents, copyright_info.prefix, copyright_info.suffix)

    with open(output_path, 'wt') as file:
        file.writelines(updated_contents)


def _remove_copyright(initial_contents, prefix, suffix):
    num_lines = len(initial_contents)

    prefix_lines = prefix.splitlines(keepends=True)
    suffix_lines = suffix.splitlines(keepends=True)

    updated_contents = []

    status = _SearchState.SEARCHING_FOR_PREFIX

    idx = 0
    while idx < num_lines:
        if status == _SearchState.SEARCHING_FOR_PREFIX:
            idx, line, status = _check_for_prefix(idx, initial_contents, prefix_lines)
            if line is not None:
                updated_contents.append(line)

        elif status == _SearchState.SEARCHING_FOR_SUFFIX:
            idx, status = _check_for_suffix(idx, initial_contents, suffix_lines)

        elif status == _SearchState.KEEP_REMAINING:
            updated_contents += initial_contents[idx:]
            break

        else:
            raise ValueError(f"status has unexpected value ({status})")

        idx += 1

    return updated_contents


def _check_for_prefix(idx, initial_contents, prefix_lines):
    line = initial_contents[idx]

    # If this line is not the start of the prefix, keep
    # the current line and keep looking
    if line != prefix_lines[0]:
        return idx, line, _SearchState.SEARCHING_FOR_PREFIX

    else:
        num_lines = len(initial_contents)
        prefix_len = len(prefix_lines)
        remaining_lines = num_lines - idx

        # If the expected prefix is larger than the remaining lines,
        # there is no prefix, and we can just grab everything else
        if prefix_len > remaining_lines:
            return idx, line, _SearchState.KEEP_REMAINING

        else:
            end_idx = idx + prefix_len
            test_lines = initial_contents[idx:end_idx]

            # If we didn't actually find the prefix, keep the current
            # line and keep looking
            if test_lines != prefix_lines:
                return idx, line, _SearchState.SEARCHING_FOR_PREFIX

            # If we did find the prefix, remove it from the contents
            else:
                idx += prefix_len - 1
                return idx, None, _SearchState.SEARCHING_FOR_SUFFIX


def _check_for_suffix(idx, initial_contents, suffix_lines):
    line = initial_contents[idx]

    # If this line is not the start of the suffix, skip
    # the current line and keep looking
    if line != suffix_lines[0]:
        return idx, _SearchState.SEARCHING_FOR_SUFFIX

    else:
        num_lines = len(initial_contents)
        suffix_len = len(suffix_lines)
        remaining_lines = num_lines - idx

        # If the expected suffix is larger than the remaining lines,
        # there is no suffix, and we will just skip everything else
        if suffix_len > remaining_lines:
            idx += remaining_lines
            return idx, _SearchState.KEEP_REMAINING

        else:
            end_idx = idx + suffix_len
            test_lines = initial_contents[idx:end_idx]

            # If we didn't actually find the suffix, skip the current
            # line and keep looking
            if test_lines != suffix_lines:
                return idx, _SearchState.SEARCHING_FOR_SUFFIX

            # If we did find the suffix, remove it from the contents
            else:
                idx += suffix_len - 1
                return idx, _SearchState.KEEP_REMAINING
