import os
import json
from .shell import shell

def load_json_file(file_name):
    """
    Loads json file
    @param file_name: filepath to JSON file
    @return: dictionary
    @raise: IO Error if JSON file does not exist or cannot be parsed
    """
    if os.path.exists(file_name):
        with open(file_name) as fname:
            #Bioschema per default downloads as html, if html ending detected, assume wrapper html tags around json
            if file_name.split(".")[-1] == "html":
                try:
                    content = fname.readlines()
                    return json.loads("".join(["".join(line.rsplit()) for line in content[1:-1]]))
                except Exception as _:
                    pass
            try:
                return json.load(fname)
            except Exception as decoder_error:
                # attempt to override decoder error in a user friendly manner
                new_decoder_error=json.decoder.JSONDecodeError(f"'{file_name}' appears to be ill formatted. Error message was: {decoder_error.msg}", decoder_error.doc, decoder_error.pos)
                raise new_decoder_error
    else:
        raise IOError("JSON file '%s' not found" % file_name)

def check_irods_object_existence(file_name, r_type):
    """
    Checks if iRods object exists
    @param file_name: iRods object (data object or collection)
    @param r_type: type of iRods resource (data object or collection)
    @raise: IO Error if irods resource does not exist or the type is not specifiec
    """
    shell_cmd = "imeta ls -{type} {obj}".format(type=r_type, obj=file_name)
    out, err, error_code = shell(shell_cmd, return_errorcode=True)

    if error_code == 4:
        print(err)
        raise IOError(
            "iRods object: '%s' not found or wrong type specification: '%s'"
            % (file_name, r_type)
        )
