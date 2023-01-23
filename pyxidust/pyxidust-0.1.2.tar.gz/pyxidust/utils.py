def change_name(extension, directory, serials):
    """Renames files in a folder via incremental serial numbers per a certain
    file extension.
    -----------
    PARAMETERS:
    -----------
    extension: str
        file extension to search for in the directory
    directory: path
        path to a directory containing files of a certain extension
    serials: path
        text file containing the starting serial number to increment
    ------
    USAGE:
    ------
    from pyxidust.utils import change_name
    change_name(extension='.jpg', directory=r'\\folder', serials=r'\\Serials.txt')
    """

    import os
    os.chdir(directory)

    with open(serials, 'r') as file:
        serial = int(file.read())

    for root, dirs, files in os.walk(directory):
        for photo in files:
            if photo.endswith(extension):
                serial += 1
                text = str(serial)
                os.rename(photo, f'{serial}{extension}')
                with open(serials, 'w') as file:
                    file.write(text)
                    
###############################################################################

def get_metadata(extension, directory):
    """Crawls a directory and returns metadata per a certain file extension.
    -----------
    PARAMETERS:
    -----------
    extension: str
        file extension to search for in the directory
    directory: path
        path to a directory containing files of a certain extension
    ------
    USAGE:
    ------
    from pyxidust.utils import get_metadata
    get_metadata(extension='.jpg', directory=r'\\folder')
    """
    
    import datetime
    import os
    import pandas
    
    name = []
    path = []
    time = []
    
    catalog = (f'{directory}\\Catalog.csv')

    # loop through directory returning the fully qualified path name to a file
    # filtered by its extension
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                # get full path of file
                location = os.path.join(root, file)
                # write file path to list
                path.append(location)
                # write file name to list
                name.append(file)
                # get UNIX time in seconds elapsed
                unix_time = os.path.getmtime(location)
                # convert UNIX time to UTC time
                utc_time = datetime.datetime.utcfromtimestamp(unix_time)
                # write UTC time to list
                time.append(utc_time)
                # read name list into data frame
                df1 = pandas.DataFrame(name, columns=['FILE_NAME'])
                # read path list into data frame
                df2 = pandas.DataFrame(path, columns=['FILE_PATH'])
                # read time list into data frame
                df3 = pandas.DataFrame(time, columns=['LAST_MODIFIED'])
                # combine data frames 1-3
                df4 = pandas.concat([df1, df2, df3], axis='columns')
                # shift index to start at one during initial crawl
                # increment this index anytime you change file type
                # or directory location to maintain a global ID
                df4.index += 1
                # set global 'ID' field name
                df4.index.name = 'ID'
                # write output to file
                df5 = df4.to_csv(catalog)
