import re

def sensor_generator(query_text, desired_pattern=".*\..*\..*", timezone="Greenwich" ):
    
    """Receives an string with queries and returns
        1. A sensor query with all query's sources; 
        2. A list of all sources in the file.
    
    This function detects specifically BigQuery table patterns inside queries.
    
    THe pattern is the following:
    
        <PROJECT_ID>.<DATASET_ID>.<TABLE_ID>
    
    Main intent is to look for 'sources' in the query:
    --------------------------------------------------------------------------
    Example 1 : SELECT * FROM project_x.dataset_y.table_z
    
                In this example, project_x.dataset_y.table_z IS a source.
            
    Example 2 : MERGE project_x.dataset_x.table_x AS current
                USING SELECT * 
                FROM       project_y.dataset_y.table_y 
                INNER JOIN project_z.dataset_z.table_z
                ON y = z                
    
                In this example, project_x.dataset_y.table_z IS NOT a source; 
                                 project_y.dataset_y.table_y IS a source; 
                                 project_z.dataset_z.table_z IS a source. 
                                 
    
    --------------------------------------------------------------------------
    Args:
        
        1. query_text (str): A query string (possibly directly from a file);
                          
            Example: 'SELECT * FROM x.y.z'
            
        2. desired_pattern (str): RegEx string containing the desired pattern to look for. Default is BigQuery Pattern.
        
            Example: ".*\..*\..*" (looks for 'project.dataset.table' pattern)
                                           
        3. timezone (str): A timezone for the datetime column of the sensor query (Big Query default is UTC)
        
            Example: 'America/Sao_Paulo'

    Returns:
        str : A text with the complete sensor query.
        list: A list with all the sources (project.dataset.table) found.
    """
    
    list_sources = []
    dict_sensors = {}
    text_sensor  = ''
    text_table   = ''
    total_tables = 0
    
    clauses_wanted  = ['JOIN', 'FROM', 'TABLE', 'UNNEST']
    clauses_ignored = ['UNNEST']
    
    #goes over the lines to find the desired pattern 'project.dataset.table'. 
    lines = query_text.split()
    for i in range(len(lines)):
        
        if (         re.search(desired_pattern, lines[i])                        \
             and     any(word in lines[i-1].upper() for word in clauses_wanted)  \
             and not any(word in lines[i-1].upper() for word in clauses_ignored)
        ):
            #if pattern is found in the way we want, then we store it.
            list_sources.append(lines[i].replace( '`', '').replace( '(', '').replace( ')', ''))

    #sort sources and remove duplicates
    list_sources = list(set(list_sources))
    list_sources.sort()
    
    for source in list_sources:
        project, dataset, table = source.split('.')
        
        if project not in dict_sensors:
            dict_sensors[project] = {}
        if dataset not in dict_sensors[project]:
            dict_sensors[project][dataset] = []
        if table not in dict_sensors[project][dataset]:
            dict_sensors[project][dataset].append(table)

    ### ---------- SENSOR STRING ---------- ###
    
    for project in dict_sensors:
        
        text_table = ''
        
        for dataset in dict_sensors[project]:

            # CHECK TABLES IN THIS PARTICULAR PROJECT.DATASET
            for i in range(len(dict_sensors[project][dataset])):
                total_tables+=1
                if i == len(dict_sensors[project][dataset])-1:
                    text_table += "'" + dict_sensors[project][dataset][i] + "'"
                else:
                    text_table += "'" + dict_sensors[project][dataset][i] + "',"

            text_sensor += (f"  SELECT table_id\n"
                            f"       , DATETIME(TIMESTAMP_MILLIS(last_modified_time), '{timezone}') AS last_modified_utc_n\n"
                            f"       , IF(DATE (TIMESTAMP_MILLIS(last_modified_time), '{timezone}') = CURRENT_DATE('{timezone}'), true, false) AS in_updated\n"
                            f"  FROM `{project}.{dataset}.__TABLES__`\n"
                            f"  WHERE table_id in ({text_table})")
                
            #IF NOT MULTIPLE DATASETS OR NOT THE LAST DATASET FROM LAST PROJECT THEN ADD 'UNION ALL' BETWEEN BLOCKS.
            if dict_sensors[project][dataset][i] != list_sources[-1].split('.')[2] or dataset != list_sources[-1].split('.')[1] :
                text_sensor = text_sensor + '\n\n  UNION ALL\n\n'
    
    #CLOSING SUBQUERIES BLOCK
    text_sensor += '\n)'
    
    #ADDING FIRST LINE (here at the end because we use the quantity of tables used from total_tables variable).
    text_sensor = 'SELECT COUNTIF(in_updated) = ' + str(total_tables) + ' AS should_continue\nFROM(\n' + text_sensor
    
    ### ---------- END SENSOR STRING ---------- ###     

    return(text_sensor, list_sources)