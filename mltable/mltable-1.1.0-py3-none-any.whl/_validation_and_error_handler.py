# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------


def _get_and_validate_download_list(download_records, ignore_not_found, logger):
    if len(download_records) == 0:
        return []
    from azureml.dataprep.native import DataPrepError, StreamInfo
    # Check the download error for each record if its user error
    actual_download_list = []
    error_list = []
    for record in download_records:
        value = record['DestinationFile']
        print(f'value {value}')
        if isinstance(value, StreamInfo):
            actual_download_list.append(value.resource_identifier)
        elif isinstance(value, DataPrepError):
            resource_identifier = value.originalValue
            if ignore_not_found and value.errorCode == "Microsoft.DPrep.ErrorValues.SourceFileNotFound":
                logger.warn("'{}' hasn't been downloaded as it was not present at the source. \
                    Download is proceeding.".format(resource_identifier))
            else:
                error_list.append((resource_identifier, value.errorCode))
        else:
            raise RuntimeError(f'Unexpected error during file download.{value}')
    print(f'error_lis {error_list}')
    if error_list:
        # this will throw ValueError for user error
        # or RuntimeError for system error based on set of errors encountered
        _download_error_handler(error_list)
    return actual_download_list


def _download_error_handler(error_list):
    def is_user_error(error: str):
        # TODO needs to check the updated rslex error code
        return error in [
            "Microsoft.DPrep.ErrorValues.SourceFileNotFound",
            "Microsoft.DPrep.ErrorValues.SourceFilePermissionDenied",
            "Microsoft.DPrep.ErrorValues.InvalidArgument",
            "Microsoft.DPrep.ErrorValues.ValueWrongKind",
            "Microsoft.DPrep.ErrorValues.SourcePermissionDenied",
            "Microsoft.DPrep.ErrorValues.DestinationPermissionDenied",
            "Microsoft.DPrep.ErrorValues.DestinationDiskFull",
            "Microsoft.DPrep.ErrorValues.FileSizeChangedWhileDownloading",
            "Microsoft.DPrep.ErrorValues.StreamInfoInvalidPath",
            "Microsoft.DPrep.ErrorValues.NoManagedIdentity",
            "Microsoft.DPrep.ErrorValues.NoOboEndpoint",
            "Microsoft.DPrep.ErrorValues.StreamInfoRequired"
        ]

    message = 'Some files have failed to download:' + '\n'.join(
        [str((file_name, error_code)) for (file_name, error_code) in error_list])
    all_user_errors = True
    system_error_msg = "System error happens during downloading: "
    for (_, error) in error_list:
        if not is_user_error(error):
            all_user_errors = False
            system_error_msg += error
            break
    raise ValueError(message) if all_user_errors else RuntimeError(system_error_msg)


# temp user error classification for rslex errors
def _classify_known_user_error_from_rslex(exception_message):
    if "InvalidUriScheme" in exception_message or \
            "StreamError(NotFound)" or \
            "DataAccessError(NotFound)" or \
            "No such host is known" or \
            "No identity was found on compute" in exception_message:
        raise ValueError(exception_message)
    elif "ExecutionError(StreamError(PermissionDenied" in exception_message:
        raise ValueError(f'Getting permission error'
                         f'please make sure proper access is configured on storage: {exception_message}')
    else:
        raise SystemError(exception_message)
