# use during iteration for operations that do not support numerals
LOWER = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
]

# use during iteration for operations that do not support numerals
UPPER = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

# use for data validation
SPECIAL = [
    r'"', r"'", '\\', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
    '_', '+', '-', '=', '{', '}', '[', ']', '|', ':', ';', '<', '>', '?', ',',
    '.', '/'
]

# use during iteration for operations that do not support numerals
LETTERS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'aa', 'bb', 'cc',
    'dd', 'ee', 'ff', 'gg', 'hh', 'ii', 'jj', 'kk', 'll', 'mm', 'nn', 'oo',
    'pp', 'qq', 'rr', 'ss', 'tt', 'uu', 'vv', 'ww', 'xx', 'yy', 'zz', 'aaa',
    'bbb', 'ccc', 'ddd', 'eee', 'fff', 'ggg', 'hhh', 'iii', 'jjj', 'kkk',
    'lll', 'mmm', 'nnn', 'ooo', 'ppp', 'qqq', 'rrr', 'sss', 'ttt', 'uuu',
    'vvv', 'www', 'xxx', 'yyy', 'zzz', 'aaaa', 'bbbb', 'cccc', 'dddd', 'eeee',
    'ffff', 'gggg', 'hhhh', 'iiii', 'jjjj', 'kkkk', 'llll', 'mmmm', 'nnnn',
    'oooo', 'pppp', 'qqqq', 'rrrr', 'ssss', 'tttt', 'uuuu', 'vvvv', 'wwww',
    'xxxx', 'yyyy', 'zzzz', 'aaaaa', 'bbbbb', 'ccccc', 'ddddd', 'eeeee',
    'fffff', 'ggggg', 'hhhhh', 'iiiii', 'jjjjj', 'kkkkk', 'lllll', 'mmmmm',
    'nnnnn', 'ooooo', 'ppppp', 'qqqqq', 'rrrrr', 'sssss', 'ttttt', 'uuuuu',
    'vvvvv', 'wwwww', 'xxxxx', 'yyyyy', 'zzzzz', 'aaaaaa', 'bbbbbb', 'cccccc',
    'dddddd', 'eeeeee', 'ffffff', 'gggggg', 'hhhhhh', 'iiiiii', 'jjjjjj',
    'kkkkkk', 'llllll', 'mmmmmm', 'nnnnnn', 'oooooo', 'pppppp', 'qqqqqq',
    'rrrrrr', 'ssssss', 'tttttt', 'uuuuuu', 'vvvvvv', 'wwwwww', 'xxxxxx',
    'yyyyyy', 'zzzzzz', 'aaaaaaa', 'bbbbbbb', 'ccccccc', 'ddddddd', 'eeeeeee',
    'fffffff', 'ggggggg', 'hhhhhhh', 'iiiiiii', 'jjjjjjj', 'kkkkkkk',
    'lllllll', 'mmmmmmm', 'nnnnnnn', 'ooooooo', 'ppppppp', 'qqqqqqq',
    'rrrrrrr', 'sssssss', 'ttttttt', 'uuuuuuu', 'vvvvvvv', 'wwwwwww',
    'xxxxxxx', 'yyyyyyy', 'zzzzzzz', 'aaaaaaaa', 'bbbbbbbb', 'cccccccc',
    'dddddddd', 'eeeeeeee', 'ffffffff', 'gggggggg', 'hhhhhhhh', 'iiiiiiii',
    'jjjjjjjj', 'kkkkkkkk', 'llllllll', 'mmmmmmmm', 'nnnnnnnn', 'oooooooo',
    'pppppppp', 'qqqqqqqq', 'rrrrrrrr', 'ssssssss', 'tttttttt', 'uuuuuuuu',
    'vvvvvvvv', 'wwwwwwww', 'xxxxxxxx', 'yyyyyyyy', 'zzzzzzzz', 'aaaaaaaaa',
    'bbbbbbbbb', 'ccccccccc', 'ddddddddd', 'eeeeeeeee', 'fffffffff',
    'ggggggggg', 'hhhhhhhhh', 'iiiiiiiii', 'jjjjjjjjj', 'kkkkkkkkk',
    'lllllllll', 'mmmmmmmmm', 'nnnnnnnnn', 'ooooooooo', 'ppppppppp',
    'qqqqqqqqq', 'rrrrrrrrr', 'sssssssss', 'ttttttttt', 'uuuuuuuuu',
    'vvvvvvvvv', 'wwwwwwwww', 'xxxxxxxxx', 'yyyyyyyyy', 'zzzzzzzzz'
]

def create_index(directory):
    """Joins file metadata (name/path/modified) with layers/layouts/maps via a
    global ID for each .aprx file in the specified directory.
    -----------
    PARAMETERS:
    -----------
    directory: path
        path to a directory containing files with an .aprx extension
    ------
    USAGE:
    ------
    from pyxidust.arc import create_index
    create_index(directory=r'\\folder')
    """
    
    import arcpy
    import pandas
    from pandas import merge, read_csv
    from pyxidust.utils import get_metadata
    
    # get file name/path/modified
    get_metadata('.aprx', directory)
    # read file metadata into pandas dataframe ('df')
    df = read_csv(f'{directory}\\Catalog.csv')
    # create list of ArcGIS PRO project objects
    projects = [arcpy.mp.ArcGISProject(i) for i in df['FILE_PATH']]

    # create new lists for each project chunk
    # when using outside of function scope
    map_frames = []
    map_layers = []
    map_layouts = []
    
    # return tuples with ID/project object
    for i in enumerate(projects, start=1):
        # tuple[-1] = project object
        project = i[-1]
        # tuple[-2] = global ID
        identifier = i[-2]
        # arcpy functions
        maps = project.listMaps()
        layouts = project.listLayouts()
        # loop projects; return ID/attributes
        # separated by pipe symbol; write to list
        for _maps in maps:
            layers = _maps.listLayers()
            map_text = str(identifier) + '|' + _maps.name
            map_frames.append(map_text)
            for layer in layers:
                layer_text = str(identifier) + '|' + layer.name
                map_layers.append(layer_text)
        for layout in layouts:
            layout_text = str(identifier) + '|' + layout.name
            map_layouts.append(layout_text)

    # write field names/attributes to newlines
    with open(f'{directory}\\Maps.csv', 'w+') as file:
        file.write('ID|MAP_NAME\n')
        for s in map_frames:
            file.write('%s\n' % s)
    with open(f'{directory}\\Layers.csv', 'w+') as file:
        file.write('ID|LAYER_NAME\n')
        for s in map_layers:
            file.write('%s\n' % s)
    with open(f'{directory}\\Layouts.csv', 'w+') as file:
        file.write('ID|LAYOUT_NAME\n')
        for s in map_layouts:
            file.write('%s\n' % s)
    
    # read-in structured newlines to perform merge assigning the global
    # ID to the index values of the dataframes
    df_info = read_csv(f'{directory}\\Catalog.csv', ',', index_col='ID')
    df_layers = read_csv(f'{directory}\\Layers.csv', '|', index_col='ID')
    df_layouts = read_csv(f'{directory}\\Layouts.csv', '|', index_col='ID')
    df_maps = read_csv(f'{directory}\\Maps.csv', '|', index_col='ID')
    
    # join file metadata to ArcGIS attributes and write to csv; output files
    # can be imported as separate sheets into an Excel notebook to create a
    # finished product; Excel does not support the number of rows created when
    # joining as one table with many-to-many relationships
    layers_merge = merge(df_layers, df_info, how='left', on=None,
        left_on='ID', right_on='ID')
    layers_merge.to_csv(f'{directory}\\LayersJoined.csv', sep='|')
    layouts_merge = merge(df_layouts, df_info, how='left', on=None,
        left_on='ID', right_on='ID')
    layouts_merge.to_csv(f'{directory}\\LayoutsJoined.csv', sep='|')
    maps_merge = merge(df_maps, df_info, how='left', on=None,
        left_on='ID', right_on='ID')
    maps_merge.to_csv(f'{directory}\\MapsJoined.csv', sep='|')
    
###############################################################################

def csv_to_gdb(csv, gdb, table):
    """Converts a .csv file to a geodatabase table.
    -----------
    PARAMETERS:
    -----------
    csv: path
        path to a .csv file
    gdb: path
        path to an ArcGIS geodatabase (workspace)
    table: str
        name of the geodatabase output table
    ------
    USAGE:
    ------
    from pyxidust.arc import csv_to_gdb
    csv_to_gdb(csv=r'\\.csv', gdb=r'\\.gdb', table='Output')
    """
    from arcpy.conversion import TableToTable
    TableToTable(csv, gdb, table)

###############################################################################

def cubic_volume(original, current, gdb, polygons):
    """Calculates volume in cubic yards using a cut/fill operation on two input
    rasters with the same cell size and coordinate system.
    -----------
    PARAMETERS:
    -----------
    original: path
        Fully-qualified/raw file path to a GRID of the original surface
    current: path
        Fully-qualified/raw file path to a GRID of the current surface
    gdb: path
        Fully-qualified/raw path to an ArcGIS geodatabase to store the results
    polygons: str
        Polygon feature class in the geodatabase to set boundaries of cut/fill
    ------
    USAGE:
    ------
    from pyxidust import *
    from pyxidust.arc import cubic_volume
    cubic_volume(original=r'\\', current=r'\\', gdb=r'\\.gdb', polygons='poly')
    """
    import arcpy
    from arcpy.ddd import CutFill
    from arcpy.sa import ExtractByMask
    from arcpy.analysis import Statistics
    from arcpy.da import SearchCursor, UpdateCursor
    from arcpy.conversion import FeatureClassToFeatureClass
    from arcpy.management import AddField, CalculateField, DeleteField, Merge
    
    # need workspace to use list methods
    arcpy.env.workspace = gdb
    
    # get required licenses
    arcpy.CheckOutExtension('SPATIAL')
    arcpy.CheckOutExtension('3D')
    
    # full path to input polygons
    boundaries = (f'{gdb}\\{polygons}')
    
    # letter iterator to workaround
    # numerals in filenames limitation
    counter = iter(LETTERS)
    
    # stores letters for each row in search cursor;
    # links polygons to rasters/tables via filename
    suffixes = []
    
    # geometry token SHAPE@ accesses polygon objects
    with SearchCursor(boundaries, ['SHAPE@']) as cursor:
        # loop polygon objects
        for row in cursor:
            # letter per iteration
            letter = next(counter)
            # store per iteration
            suffixes.append(letter)
            # unique letter per filename
            shapefile = (f'input_{letter}')
            # create a feature class for each row of the polygons
            FeatureClassToFeatureClass(in_features=row, out_path=gdb,
                out_name=shapefile)
    
    # create new iterator for loop
    raster_iterator = iter(suffixes)
    # get previous output with wild_card='input*'
    for fc in arcpy.ListFeatureClasses('input*'):
        try:
            # try/catch to handle stop iteration
            raster_suffix = next(raster_iterator)
            raster = (f'{gdb}\\cf_{raster_suffix}')
            # create subset rasters for original/current data within polygons
            before_clip = ExtractByMask(in_raster=original, in_mask_data=fc)
            after_clip = ExtractByMask(in_raster=current, in_mask_data=fc)
            # cut/fill produces AREA field in sq ft and VOLUME in cubic feet
            CutFill(in_before_surface=before_clip, in_after_surface=after_clip,
                out_raster=raster)
        except StopIteration:
            pass
    
    # create new iterator for loop
    stats_iterator = iter(suffixes)
    # get previous output with wild_card='cf*'
    for fc in arcpy.ListRasters('cf*'):
        try:
            # try/catch to handle stop iteration
            stats_suffix = next(stats_iterator)
            stats = (f'{gdb}\\stats_{stats_suffix}')
            # calculate cubic volume per raster
            CalculateField(in_table=fc, field='VOL_CUB_YDS',
                expression="!VOLUME!/27", expression_type='PYTHON3',
                field_type='DOUBLE')
            # calculate cubic volume sum per raster
            Statistics(in_table=fc, out_table=stats,
                statistics_fields=[['VOL_CUB_YDS', 'SUM']])
        except StopIteration:
            pass
    
    # dict for suffix:sum values
    sum_values = {}
    # create new iterator for loop
    search_iterator = iter(suffixes)
    # get previous output with wild_card='stats*'
    for fc in arcpy.ListTables('stats*'):
        # access field values and store in dict
        with SearchCursor(fc, ['SUM_VOL_CUB_YDS']) as cursor:
            # loop stats tables
            for row in cursor:
                # drop decimal values
                value = round(row[0])
                # get string value; drop negative
                sum_value = (str(value)).replace('-', '')
                search_suffix = next(search_iterator)
                sum_values.update({search_suffix: sum_value})
    
    # get previous output with wild_card='input*'
    for fc in arcpy.ListFeatureClasses('input*'):
        # get filename suffixes
        name_suffix = fc.split('_')
        # extract value from tuple
        loop_value = name_suffix[1]
        # add new field to calculate labels
        AddField(in_table=fc, field_name='LABEL2', field_type='TEXT',
            field_length=256)
        # add new field to store labels
        AddField(in_table=fc, field_name='LABEL', field_type='TEXT',
            field_length=256)
        # write volumes from stats to polygons
        with UpdateCursor(fc, ['LABEL']) as cursor:
            # loop stats tables
            for row in cursor:
                # link datasets through suffix
                for key, value in sum_values.items():
                    if key == loop_value:
                        # carryover value from raster
                        CalculateField(in_table=fc, field='LABEL2',
                            expression=value, expression_type='PYTHON3')
                        # calculate again to add 'CY'
                        CalculateField(in_table=fc, field='LABEL',
                            expression="!LABEL2! + ' CY'",
                            expression_type='PYTHON3')
                        # drop unwanted 'LABEL2' field from table
                        DeleteField(in_table=fc, drop_field='LABEL2')
    
    # get input polygon filenames and merge into final result
    datasets = [fc for fc in arcpy.ListFeatureClasses('input*')]
    results = (f'{gdb}\\CubicVolume')
    Merge(inputs=datasets, output=results)
    
    # check-in licenses
    arcpy.CheckInExtension('SPATIAL')
    arcpy.CheckInExtension('3D')

###############################################################################

def excel_to_gdb(workbook, gdb, table, sheet=None):
    """Converts a Microsoft Excel workbook sheet to an ArcGIS geodatabase table.
    -----------
    PARAMETERS:
    -----------
    workbook: path
        path to a Microsoft Excel workbook in .xlsx format
    gdb: path
        path to an ArcGIS geodatabase (workspace)
    table: str
        name of the geodatabase output table
    sheet: str
        workbook sheet name; used if the sheet to be converted to table is not
        the first sheet in the workbook
    ------
    USAGE:
    ------
    from pyxidust.arc import excel_to_gdb
    excel_to_gdb(workbook=r'\\.xlsx', gdb=r'\\.gdb', table='Output',
        sheet='Sheet 1')
    """
    
    import os
    from pandas import DataFrame, read_excel
    from arcpy.conversion import TableToTable
    
    csv = (f'{os.getcwd()}\\excel_to_gdb.csv')
    
    if sheet != None:
        df = DataFrame(read_excel(workbook, sheet_name=sheet))
        df.to_csv(csv)
        TableToTable(csv, gdb, table)
    else:
        df = DataFrame(read_excel(workbook))
        df.to_csv(csv)
        TableToTable(csv, gdb, table)
        
    os.remove(csv)
    
###############################################################################

def plot_csv(pro_obj, map_name, csv, crs, output, x_name, y_name, z_name=None):
    """Converts X/Y/Z coordinates in a .csv file to a shapefile and adds it to
    a map in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    csv: path
        Fully-qualified/raw file path to a .csv file containing X/Y data
    crs: path
        Fully-qualified/raw file path to an ArcGIS projection file of the
        desired output coordinate reference system
    output: path
        Fully-qualified/raw file path to the desired output shapefile
    x_name: str
        Name of field containing X coordinates to import
    y_name: str
        Name of field containing Y coordinates to import
    z_name: str
        Name of field containing Z coordinates to import
    ------
    USAGE:
    ------
    import arcpy
    from pyxidust.arc import plot_csv
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    # z-values are optional
    plot_csv(pro_obj=project_, map_name='Map', csv=r'\\.csv', crs=r'\\.prj',
        output=r'\\.shp', x_name='X', y_name='Y', z_name=None='Z')
    """
    
    import arcpy
    import os
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    
    if z_name != None:
        arcpy.management.MakeXYEventLayer(table=csv, in_x_field=x_name,
            in_y_field=y_name, out_layer=r'memory\\event',
            spatial_reference=crs, in_z_field=z_name)
    if z_name == None:
        arcpy.management.MakeXYEventLayer(table=csv, in_x_field=x_name,
            in_y_field=y_name, out_layer=r'memory\\event',
            spatial_reference=crs)
        
    plot = arcpy.management.CopyFeatures(in_features=r'memory\\event',
        out_feature_class=output)
    features = arcpy.management.MakeFeatureLayer(in_features=plot,
        out_layer='plot')
    
    _layer = features.getOutput(0)
    _map.addLayer(_layer)
    _project.save()
    
###############################################################################

def plot_excel(workbook, pro_obj, map_name, crs, output, x_name, y_name,
        z_name=None, sheet=None):
    """Converts X/Y/Z coordinates in a spreadsheet workbook to a shapefile and
    adds it to a map in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    workbook: path
        path to a spreadsheet workbook in xls/xlsx/xlsm/xlsb/odf/ods/odt format
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    crs: path
        Fully-qualified/raw file path to an ArcGIS projection file of the
        desired output coordinate reference system
    output: path
        Fully-qualified/raw file path to the desired output shapefile
    x_name: str
        Name of field containing X coordinates to import
    y_name: str
        Name of field containing Y coordinates to import
    z_name: str
        Name of field containing Z coordinates to import
    sheet: str
        individual spreadsheet name; used if the sheet to be converted is not
        the first sheet in the workbook
    ------
    USAGE:
    ------
    import arcpy
    from pyxidust.arc import plot_excel
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    # z-values and sheet name are optional
    plot_excel(workbook=r'\\.xlsx', pro_obj=project_, map_name='Map',
        crs=r'\\.prj', output=r'\\.shp', x_name='X', y_name='Y', z_name='Z',
        sheet='Sheet1')
    """
    
    import os
    from pyxidust.arc import csv_plot
    from pandas import DataFrame, read_excel
    
    plot = (f'{os.getcwd()}\\plot.csv')
    
    if sheet == None and z_name == None:
        df = DataFrame(read_excel(workbook))
        df.to_csv(plot)
        csv_plot(pro_obj=pro_obj, map_name=map_name, csv=plot, crs=crs,
            output=output, x_name=x_name, y_name=y_name)
    elif sheet != None and z_name == None:
        df = DataFrame(read_excel(workbook, sheet_name=sheet))
        df.to_csv(plot)
        csv_plot(pro_obj=pro_obj, map_name=map_name, csv=plot, crs=crs,
            output=output, x_name=x_name, y_name=y_name)
    elif sheet == None and z_name != None:
        df = DataFrame(read_excel(workbook))
        df.to_csv(plot)
        csv_plot(pro_obj=pro_obj, map_name=map_name, csv=plot, crs=crs,
            output=output, x_name=x_name, y_name=y_name, z_name=z_name)
    elif sheet != None and z_name != None:
        df = DataFrame(read_excel(workbook, sheet_name=sheet))
        df.to_csv(plot)
        csv_plot(pro_obj=pro_obj, map_name=map_name, csv=plot, crs=crs,
            output=output, x_name=x_name, y_name=y_name, z_name=z_name)
        
    os.remove(plot)
    
###############################################################################

def place_anno(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust, gdb,
             suffix):
    """Sets reference scale from a layer in an ArcGIS PRO project and creates
    annotation feature classes for all layers with visible labels.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    lay_name: str
        Layout name as it appears in the catalog pane (default is 'Layout')
    fra_name: str
        Frame name as it appears in the layout TOC (default is 'Map Frame')
    lyr_idx: int
        Index position of a layer in the map TOC layer stack (0, 1, ...)
    adjust: float
        value used to fine-tune layout scale; value will be multiplied by the
        map frame camera scale; use a value less than 1 to decrease scale and a
        value more than 1 to increase scale (0.7, 1.2)
    gdb: path
        output geodatabase for the annotation features
    suffix: str
        letter added to all new annotation feature class names
    --------
    RETURNS:
    --------
    _extent:
        ArcGIS extent object
    scale:
        ArcGIS environment/map/camera scale used as conversion scale for anno
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    # returns extent, scale; unpack or call without variables
    extent,scale = place_anno(pro_obj=project_, map_name='Map',
        lay_name='Layout', fra_name='Map Frame', lyr_idx=0, adjust=1.1,
        gdb=r'\\.gdb', suffix='A')
    """
    
    import arcpy
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    _layout = _project.listLayouts(lay_name)[0]
    _frame = _layout.listElements('MAPFRAME_ELEMENT', fra_name)[0]
    _layer = _map.listLayers()[lyr_idx]
    
    _extent = _frame.getLayerExtent(_layer, True)
    _frame.camera.setExtent(_extent)
    _frame.camera.scale *= adjust
    arcpy.env.referenceScale = _frame.camera.scale
    _map.referenceScale = arcpy.env.referenceScale
    scale = _map.referenceScale
    _project.save()
    
    arcpy.cartography.ConvertLabelsToAnnotation(input_map=_map,
        conversion_scale=scale, output_geodatabase=gdb, anno_suffix=suffix,
        extent=_extent)
    
    return _extent, scale

###############################################################################

def print_info(pro_obj):
    """Prints map/layout/layer names and data sources in an ArcGIS PRO project.
    Useful for troublesome projects that will not open due to memory issues.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    print_info(pro_obj=project_)
    """
    
    import arcpy
    
    _project = pro_obj
    _layouts = [layout.name for layout in _project.listLayouts()]
    
    print(f'Layout names: {_layouts}\n')
    
    for _id, _map in enumerate(_project.listMaps(), start=1):
        for _layer in _map.listLayers():
            if _layer.isFeatureLayer:
                print(f'Map #{_id} ({_map.name})')
                print(f'{_layer.name} layer source: {_layer.dataSource}')
                
###############################################################################

def print_layers(pro_obj, map_name):
    """Prints the properties of all layers in a map in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    print_layers(pro_obj=project_, map_name='Map')
    """
    
    import arcpy
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    _layers = _map.listLayers()
    
    for _layer in _layers:
        if _layer.isGroupLayer == False:
            print('')
            print('_' * 79)
            print('')
            print('')
            if _layer.supports('NAME'):
                print(f'Layer name: {_layer.name}')
            if _layer.supports('LONGNAME'):
                print(f'Group name: {_layer.longName}')
            if _layer.is3DLayer:
                print(f'3D layer = True')
            if _layer.isWebLayer:
                print(f'Web layer = True')
            if _layer.isSceneLayer:
                print(f'Scene layer = True')
            if _layer.isTimeEnabled:
                print(f'Time enabled = True')
            if _layer.isRasterLayer:
                print(f'Raster layer = True')
            if _layer.isBasemapLayer:
                print(f'Basemap layer = True')
            if _layer.isFeatureLayer:
                print(f'Feature layer = True')
            if _layer.isBroken:
                print(f'Broken data source = True')
            if _layer.supports('VISIBLE'):
                print(f'Visible = {_layer.visible}')
            if _layer.isNetworkAnalystLayer:
                print(f'Network analyst layer = True')
            if _layer.isNetworkDatasetLayer:
                print(f'Network dataset layer = True')
            if _layer.supports('SHOWLABELS'):
                print(f'Labels on = {_layer.showLabels}')
            print('')
            if _layer.supports('TIME'):
                print(f'Time: {_layer.time}')
            if _layer.supports('CONTRAST'):
                print(f'Contrast: {_layer.contrast}')
            if _layer.supports('BRIGHTNESS'):
                print(f'Brightness: {_layer.brightness}')
            if _layer.supports('TRANSPARENCY'):
                print(f'Transparency: {_layer.transparency}')
            if _layer.supports('MINTHRESHOLD'):
                print(f'Min display scale: {_layer.minThreshold}')
            if _layer.supports('MAXTHRESHOLD'):
                print(f'Max display scale: {_layer.maxThreshold}')
            if _layer.supports('DEFINITIONQUERY'):
                print(f'Query: {_layer.definitionQuery}')
            print('')
            if _layer.supports('URI'):
                print(f'Universal resource indicator: {_layer.URI}')
            if _layer.supports('DATASOURCE'):
                print(f'Source: {_layer.dataSource}')
            if _layer.supports('CONNECTIONPROPERTIES'):
                print(f'Connection: {_layer.connectionProperties}')
            if _layer.supports('METADATA'):
                print('')
                meta = _layer.metadata
                print(f'Metadata title: {meta.title}')
                print(f'Metadata description: {meta.description}')
                
###############################################################################

def set_default(pro_obj, home, gdb, toolbox):
    """Updates home folder/default geodatabase/toolbox in an ArcGIS PRO project.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    home: path
        path to a new home folder for the PRO project
    gdb: path
        path to a new default geodatabase for the PRO project
    toolbox: path
        path to a new default toolbox for the PRO project
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    set_default(pro_obj=project_, home=r'\\folder', gdb=r'\\.gdb',
        toolbox=r'\\.tbx')
    """
    
    import arcpy
    
    _project = pro_obj
    _project.homeFolder = home
    _project.defaultGeodatabase = gdb
    _project.defaultToolbox = toolbox
    _project.save()
    
###############################################################################

def turn_off(pro_obj, map_name, lyr_idx):
    """Turns off layers in a map in an ArcGIS PRO project if the layer index
    position is found in the input list.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    lyr_idx: list
        List of integers representing index positions of layers in the map
        table of contents layer stack to turn off
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    turn_off(pro_obj=project_, map_name='Map', lyr_idx=[0,1,2])
    """
    
    import arcpy
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    
    for i in lyr_idx:
        index = int(i)
        _layer = _map.listLayers()[index]
        if _layer.isFeatureLayer:
            _layer.visible = False
    _project.save()
    
###############################################################################

def zoom_to(pro_obj, map_name, lay_name, fra_name, lyr_idx, adjust):
    """Sets reference scale from a layer in an ArcGIS PRO project and zooms the
    layout to the layer extent.
    -----------
    PARAMETERS:
    -----------
    pro_obj:
        ArcGIS project object
    map_name: str
        Map name as it appears in the catalog pane (default is 'Map')
    lay_name: str
        Layout name as it appears in the catalog pane (default is 'Layout')
    fra_name: str
        Frame name as it appears in the layout TOC (default is 'Map Frame')
    lyr_idx: int
        Index position of a layer in the map TOC layer stack (0, 1, ...)
    adjust: float
        value used to fine-tune layout scale; value will be multiplied by the
        map frame camera scale; use a value less than 1 to decrease scale and a
        value more than 1 to increase scale (0.7, 1.2)
    ------
    USAGE:
    ------
    import arcpy
    project_ = arcpy.mp.ArcGISProject(r'\\.aprx')
    zoom_to(pro_obj=project_, map_name='Map', lay_name='Layout',
        fra_name='Map Frame', lyr_idx=0, adjust=1.1)
    """
    
    import arcpy
    
    _project = pro_obj
    _map = _project.listMaps(map_name)[0]
    _layout = _project.listLayouts(lay_name)[0]
    _frame = _layout.listElements('MAPFRAME_ELEMENT', fra_name)[0]
    _layer = _map.listLayers()[lyr_idx]
    
    _extent = _frame.getLayerExtent(_layer, True)
    _frame.camera.setExtent(_extent)
    _frame.camera.scale *= adjust
    arcpy.env.referenceScale = _frame.camera.scale
    _map.referenceScale = arcpy.env.referenceScale
    scale = _map.referenceScale
    _project.save()
