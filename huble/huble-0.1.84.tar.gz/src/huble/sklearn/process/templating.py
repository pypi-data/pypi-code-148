def return_function(node):
    if node["data"]["value"] == "Remove NAN values":
        return temp_remove_nan_values(node['data']['parameters'])
    elif node["data"]["value"] == "Replace NAN values":
        return temp_replace_nan_values(node['data']['parameters'])
    elif node["data"]["value"] == "Dropping rows or columns":
        return temp_drop_rows_columns(node['data']['parameters'])
    elif node["data"]["value"] == "Remove Outliers":
        return temp_remove_outliers(node['data']['parameters'])
    elif node["data"]["value"] == "Drop Duplicates":
        return temp_drop_duplicates(node['data']['parameters'])
    elif node["data"]["value"] == "Change Data Type":
        return temp_change_data_type(node['data']['parameters'])
    elif node["data"]["value"] == "Round Data":
        return temp_round_data(node['data']['parameters'])
    elif node["data"]["value"] == "Filter DataFrame":
        return temp_filter_dataframe(node['data']['parameters'])
    elif node["data"]["value"] == "Truncate DataFrame":
        return temp_truncate_dataframe(node['data']['parameters'])
    elif node["data"]["value"] == "Sort Values":
        return temp_sort_values(node['data']['parameters'])
    elif node["data"]["value"] == "Transpose DataFrame":
        return temp_transpose()
    elif node["data"]["value"] == "Min Max Scaler":
        return temp_min_max_scale(node['data']['parameters'])
    elif node["data"]["value"] == "Max Abs Scaler":
        return temp_max_abs_scale(node['data']['parameters'])
    elif node["data"]["value"] == "Robust Scaler":
        return temp_robust_scale(node['data']['parameters'])
    elif node["data"]["value"] == "Standard Scaler":
        return temp_standard_scale(node['data']['parameters'])
    elif node["data"]["value"] == "Normalization":
        return temp_normalize(node['data']['parameters'])
    elif node["data"]["value"] == "Ordinal Encoding":
        return temp_ordinal_encode(node['data']['parameters'])
    elif node["data"]["value"] == "One Hot Encoding":
        return temp_one_hot_encode(node['data']['parameters'])
    elif node["data"]["value"] == "Remove Mismatch Data":
        return temp_remove_mismatch_data(node['data']['parameters'])
    elif node["data"]["value"] == "Rename Columns":
        return temp_rename_columns(node['data']['parameters'])
    elif node["data"]["value"] == "Select Columns":
        return temp_select_columns(node['data']['parameters'])
    elif node["data"]["value"] == "Clean Column Names":
        return temp_clean_column_names(node['data']['parameters'])
    elif node["data"]["value"] == "Clip":
        return temp_clip(node['data']['parameters'])
    elif node["data"]["value"] == "Merge":
        return temp_merge(node['data']['parameters'])
    elif node["data"]["value"] == "Clean Data":
        return temp_clean_data(node['data']['parameters'])
    elif node["data"]["value"] == "Split":
        return temp_split(node['data']['parameters'])

def temp_remove_nan_values(params):
    subset=[]
    for i in range(len(params['subset'])):
        subset.append(params['subset'][i]['value'])
    parameters = {
        "axis": params["axis"],
        "how": params["how"],
        "inplace": params["inplace"],
        "subset": subset,
    }
    return f"data = huble.sklearn.remove_nan_values(data=data,parameters={parameters})"


def temp_replace_nan_values(params):
    parameters = {
        "missing_values" : params['missing_values'], 
        "strategy" : params['strategy'],
        "fill_value" : params['fill_value'],
    }
    return f"data = huble.sklearn.replace_nan_values(data=data, column='{params['column']}', parameters={parameters})"

def temp_drop_rows_columns(params):
    labels=[]
    for i in range(len(params['labels'])):
        labels.append(params['labels'][i]['value'])

    parameters = {
        "labels" : labels,
        "axis" : params['axis'],
        "inplace" : params['inplace'],
        "errors" : params['errors'],
    }
    return f"data = huble.sklearn.drop_rows_columns(data=data,parameters={parameters})"

def temp_remove_outliers(params):
    columns=[]
    for i in range(len(params['columns'])):
        columns.append(params['columns'][i]['value'])
    return f"data = huble.sklearn.remove_outliers(data=data,columns={columns})"

def temp_drop_duplicates(params):
    subset=[]
    for i in range(len(params['subset'])):
        subset.append(params['subset'][i]['value'])
    parameters = {
        "subset" : subset, 
        "keep" : params['keep'],
        "inplace" : params['inplace'],
        "ignore_index" : params['ignore_index'],
    }
    return f"data = huble.sklearn.drop_duplicates(data=data,parameters={parameters})"


def temp_change_data_type(params):
    parameters = {
        "dtype" : params['data type'], 
        "copy" : params['copy'], 
        "errors" : params['errors'],
    }
    return f"data = huble.sklearn.change_data_type(data=data,column={params['column']}, parameters={parameters})"


def temp_round_data(params):
    parameters = {
        "decimals" : params['decimals'],
    }
    return f"data = huble.sklearn.round_data(data=data, parameters={parameters})"


def temp_filter_dataframe(params):
    items=[]
    for i in range(len(params['items'])):
        items.append(params['items'][i]['value'])
    parameters = {
        "items" : items,
        "like" : params['like'],
        "axis" : params['axis'],
    }
    return f"data = huble.sklearn.filter_dataframe(data=data, parameters={parameters})"


def temp_truncate_dataframe(params):
    parameters = {
        "before" : params['before'], 
        "after" : params['after'], 
        "copy" : params['copy'], 
        "axis" : params['axis'],
    }
    return f"data = huble.sklearn.truncate_datfarame(data=data, parameters={parameters})"


def temp_sort_values(params):
    by=[]
    for i in range(len(params['by'])):
        by.append(params['by'][i]['value'])
    parameters = {
        "by" : by,
        "axis" : params['axis'],
        "ascending" : params['ascending'],
        "inplace" : params['inplace'],
        "kind" : params['kind'],
        "na_position" : params['na_position'],
        "ignore_index" : params['ignore_index'],
    }
    return f"data = huble.sklearn.sort_values(data=data, parameters={parameters})"


def temp_transpose():
    return f"data = huble.sklearn.transpose(data=data)"


def temp_min_max_scale(params):
    parameters = {
        "feature_range" : params['feature_range'], 
        "copy" : params['copy'], 
        "clip" : params['clip'],
    }
    return f"data = huble.sklearn.min_max_scalar(data=data, columns={params['columns']}, parameters={parameters})"


def temp_max_abs_scale(params):
    parameters = {
        "copy" : params['copy'],
    }
    return f"data = huble.sklearn.max_abs_scalar(data=data, columns={params['columns']}, parameters={parameters})"


def temp_robust_scale(params):
    columns=[]
    for i in range(len(params['column'])):
        columns.append(params['column'][i]['value'])
    parameters = {
        "with_centering" : params['with_centering'], 
        "with_scaling" : params['with_scaling'], 
        "copy" : params['copy'], 
        "unit_variance" : params['unit_variance'], 
        "quantile_range" : params['quantile_range'],
    }
    return f"data = huble.sklearn.robust_scalar(data=data, column={columns}, parameters={parameters})"


def temp_standard_scale(params):
    parameters = {
        "copy" : params['copy'], 
        "with_mean" : params['with_mean'], 
        "with_std" : params['with_std'],
    }
    return f"data = huble.sklearn.standard_scalar(data=data, column={params['column']}, parameters={parameters})"


def temp_normalize(params):
    columns = params['columns']
    parameters = {
        "norm" : params['norm'], 
        "copy" : params['copy'],
    }
    return f"data = huble.sklearn.normalize(data=data, columns={columns}, parameters={parameters})"


def temp_ordinal_encode(params):
    columns=[]
    for i in range(len(params['columns'])):
        columns.append(params['columns'][i]['value'])
    parameters = {
        "categories" : params['categories'], 
        "dtype" : params['dtype'], 
        "handle_unknown" : params['handle_unknown'], 
        "unknown_value" : params['unknown_value'], 
        "encoded_missing_value" : params['encoded_missing_value'],
    }
    return f"data = huble.sklearn.ordinal_encode(data=data, columns={columns}, parameters={parameters})"


def temp_one_hot_encode(params):
    columns=[]
    for i in range(len(params['columns'])):
        columns.append(params['columns'][i]['value'])
    parameters = {
        "categories" : params['categories'], 
        "dtype" : params['dtype'], 
        "handle_unknown" : params['handle_unknown'], 
        "sparse" : params['sparse'], 
        "min_frequency" : params['min_frequency'], 
        "max_categories" : params['max_categories'],
    }
    return f"data = huble.sklearn.one_hot_encode(data=data, columns={columns}, parameters={parameters})"

def temp_remove_mismatch_data(params):
    parameters = {
        "exceptions" : params['exceptions'],
    }
    return f"data = huble.sklearn.remove_mismatch_data(data=data, parameters={parameters})"

def temp_rename_columns(params):
    parameters = {
        "mapper" : params['mapper'], 
        "axis" : params['axis'],
        "errors" : params['errors'],
    }
    return f"data = huble.sklearn.rename_columns(data=data, parameters={parameters})"

def temp_select_columns(params):
    parameters = {
        "include" : params['include'], 
        "exclude" : params['exclude'],
    }
    return f"data = huble.sklearn.select_columns(data=data, parameters={parameters})"

def temp_clean_column_names(params):
    return f"data = huble.sklearn.clean_column_names(data=data)"

def temp_clip(params):
    parameters = {
        "lower" : params['lower'], 
        "upper" : params['upper'],
        "axis"  : params['axis'],
    }
    return f"data = huble.sklearn.clip(data=data, parameters={parameters})"

def temp_merge(params):
    parameters = {
        "right" : params['right'], 
        "how" : params['how'],
        "on" : params['on'], 
        "left_on" : params['left_on'],
        "right_on" : params['right_on'], 
        "sort" : params['sort'],
    }
    return f"data = huble.sklearn.merge(data=data, parameters={parameters})"

def temp_clean_data(params):
    return f"data = huble.sklearn.clean_data(data=data)"

def temp_split(params):
    return f"data = huble.sklearn.split(data=data)"
