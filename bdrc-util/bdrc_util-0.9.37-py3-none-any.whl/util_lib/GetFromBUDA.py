#!/usr/bin/env python3

"""
Library routine to get volume information from BUDA
"""
import os.path
import re
import requests
import sys
from requests import Response

IG_OLD_HACK_PREFIX = 'I'


def its_a_hack(test_str: str):
    """
    Returns true if the input is 4 digits, false otherwise
    :param test_str:
    :return:
    """
    hack_pattern = re.match('^\d{4}$', test_str)
    return hack_pattern is not None


def old_hack_get_ig_disk(image_group_id: str) -> str:
    """
    Copied from volume-manifest-builder.
    :param image_group_id:
    :type image_group_id: str
    Some old image groups in eXist **and BUDA** are encoded WorkRID-Innn, but their real name on disk is
    WorkRID-nnnn. this detects their cases, and returns the suffix of the disk folder they actually
    exist in. This is a gross hack, we should either fix the archive repository, or have the
    BUDA APIs adjust for this.
    """
    if 0 == len(image_group_id):
        return image_group_id

    pre, rest = image_group_id[0], image_group_id[1:]
    return rest if pre == IG_OLD_HACK_PREFIX and its_a_hack(rest) else image_group_id


def get_buda_ig_from_disk(image_group_path: str):
    """
    Get the catalog image group name from the disk name
    :param image_group_path: path to an image group directory
    :return: the image group reference, without the path, and without the workRID
    """

    # if there is no hyphen, the how string is returned the first list position (list[0])
    with_hyphen: [] = image_group_path.split('-')

    # get non-directory part of first segment after *the last* hyphen (or the whole thing if no hyphen at all)
    first_post_hyphen: str = os.path.basename(with_hyphen[len(with_hyphen) - 1])

    return IG_OLD_HACK_PREFIX + first_post_hyphen if its_a_hack(first_post_hyphen) else first_post_hyphen


def get_disk_volumes_in_work(work_rid: str, transform_disk: bool = True) -> []:
    """
    BUDA LDS-PDI implementation
    :param: work_rid
    :return: list of dicts of 'vol_seq_in_work, vol_label' entries, where vol_label is the (potentially different)
    disk directory of an image group.
    """

    vol_info = []

    request_url: str = f'https://purl.bdrc.io/query/table/volumesForInstance'
    request_args = dict(R_RES=f"bdr:{work_rid}", format="json")

    # pattern from https://www.programcreek.com/python/example/68989/requests.HTTPError
    try:
        buda_vol_resp: Response = requests.get(request_url, request_args)
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return None
        else:
            raise

    vol_ids = buda_vol_resp.json()
    for vol_id in vol_ids['results']['bindings']:
        _vol_names = vol_id['volid']['value'].split('/')
        _vol_name = _vol_names[len(_vol_names) - 1]
        vol_info.append(dict(vol_seq_in_work=int(vol_id['volnum']['value']),
                             vol_label=old_hack_get_ig_disk(_vol_name) if transform_disk else _vol_name))

    return vol_info


def get_ig_folders_from_igs():
    """
    Call this functionality from the command line.
    Usage gget_disk_ig_dir_from_BUDA worknum [anystring]
    If [anystring] is present, the image group is NOT
    processed through the old hack
    :return:
    """

    # second argument?
    use_old_hack: bool = len(sys.argv) <= 2
    vols = [x['vol_label'] for x in get_disk_volumes_in_work(sys.argv[1], use_old_hack)]
    print('\n'.join(map(str, vols)))


def get_igs_from_ig_folders():
    """
    Given an image group folder's disk name, derive its image group name
    per the BUDA catalog
    :return:
    """
    # Anything to do?
    if len(sys.argv) == 1:
        return

    print(get_buda_ig_from_disk(sys.argv[1]))


if __name__ == "__main__":
    get_igs_from_ig_folders()
    # get_ig_folders_from_igs()
    # js: str = json.dumps(raw)
    # ig_js = json.loads(js)[]['vol_label']
    # print(ig_js)
