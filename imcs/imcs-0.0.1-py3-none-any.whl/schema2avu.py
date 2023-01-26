#!/usr/bin/env python3

import argparse
import jsonavu
import json

# import own functions
if __package__:
    from .lib.verify_functions import *
    from .lib.avu_functions import *
    from .lib.shell import *
else:
    from lib.verify_functions import *
    from lib.avu_functions import *
    from lib.shell import *

def main():
    parser = argparse.ArgumentParser()
    ruleflags = parser.add_mutually_exclusive_group(required=True)
    ruleflags.add_argument(
        "-i",
        "--ignore-duplicated-attribute",
        help="""
                           In case of existing attributes of a particular iRODS object, 
                           the script will take the new attribute from the input schema 
                           definition and add it to the iRODS object.
                           Be warned: This might lead to 'less searchable' meta data and
                                      possibly corrupted JSON output, when retrieving 
                                      the metadata.
                           """,
        action="store_true",
    )
    ruleflags.add_argument(
        "-f",
        "--force-overwrite-duplicated-attributes",
        help="""
                           In case of existing attributes of a particular iRODS object, 
                           the script will take the new attribute from the input schema 
                           definition and overwrite the previous attribute in the
                           iRODS object.
                           """,
        action="store_true",
    )


    parser.add_argument(
        "type",
        metavar="d|C|R",
        choices=["d", "C", "R"],
        help="the irods resource type [d=data objects (file), C=collection (directory), R=resources]",
    )
    parser.add_argument(
        "file", metavar="file", help="path to data object, collection or resource"
    )

    json_group = parser.add_mutually_exclusive_group(required=True)

    json_group.add_argument("-j", "--json", help="The JSON file that contains the metadata")
    json_group.add_argument("-e", "--export", action="store_true", help="Exports existing attributes of file to either JSON. The name of the JSON depends on the irods object name.")


    args = parser.parse_args()
    if args.export:
        json_data = jsonavu.avu2json(get_all_metada(args.file, args.type), "root")
        result_file_name = ".".join(args.file.split("/")[-1].split(".")[:-1])
        with open(f'{result_file_name}.json', 'w') as f:
                json.dump(json_data, f)

    else:
        data = load_json_file(args.json)

        check_irods_object_existence(args.file, args.type)
        avus = jsonavu.json2avu(data, "root")


        if args.force_overwrite_duplicated_attributes:
            existing_avus = get_all_metada(args.file, args.type)
            for triplet in avus:
                existing_attributes = [existing_avu["a"] for existing_avu in existing_avus]
                if triplet["a"] in existing_attributes:
                    matched_existing_avus = [existing_avu for existing_avu in existing_avus if existing_avu["a"] == triplet["a"]]
                    if len(matched_existing_avus) > 1:
                        triplet_to_remove = [existing_avu for existing_avu in matched_existing_avus if existing_avu["u"] == triplet["u"]]
                        remove_avu(args.file, triplet_to_remove[0], args.type)
                    else:
                        remove_avu(args.file, matched_existing_avus[0], args.type)
                populate_avu(args.file, triplet, args.type, False)
        else:
            for triplet in avus:
                populate_avu(args.file, triplet, args.type, True)

if __name__ == "__main__":
    main()
