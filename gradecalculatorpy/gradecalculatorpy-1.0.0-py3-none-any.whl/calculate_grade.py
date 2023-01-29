import pandas as pd
import os
import math

def calculate_grade(input_file_path):
    """
    When all course components are presented, calculate the course overall grade based on information provided.
    
    Parameters
    ----------
    input_file_path : str
        Path to read the saved .csv file as a string.
        Under the current working directory to avoid permission issue.
        The path should include the file name.
    
    Returns
    -------
    return_msg : double
        The course overall grade once all course components present when all grades are present.
        Otherwise return warning message
    
    Examples
    --------
    >>> calculate_grade('/DSCI524.csv')
    """
    cwd = os.getcwd()
    path = cwd + '/' + input_file_path
    course_info = pd.read_csv(path, index_col=0)
    print(course_info)

    error_msg_missing_value = 'Course component grades is missing for '
    error_msg_format = 'Course component grades with incorrect format (not 2 decimal places) for '
    grade_msg = 'Course grade is '
    percent_sign = '%'
    course_grade = 0
    return_msg = ''

    # Check if all course components have grade present
    for i, row in course_info.iterrows():
        comp = row['Components']
        grade = row['Grades (%)'] 
        weight = row['Weights (%)']
        # print(grade)
        # print(weight)

        if  math.isnan(grade):
            return_msg = error_msg_missing_value + comp
            return return_msg

        if len(str(grade).rsplit('.')[-1]) != 2:
            return_msg = error_msg_format + comp
            return return_msg

        course_grade += (grade * weight / 100)

    return_msg = grade_msg + str(round(course_grade, 2)) + percent_sign

    return return_msg