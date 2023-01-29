import pandas as pd

def load_course(input_file):
    """Loads a .csv file containing information about the course ('course.csv') and saves it in a pandas dataframe.
    
    Parameters
    ----------
    input_file : str
        Path to the .csv file as a string.
    
    Returns
    -------
    course_df : DataFrame
        A pandas dataframe containing the information from the .csv file.
    
    Examples
    --------
    >>> load_course('DSCI100.csv')
    """
    
    df = pd.read_csv(input_file, index_col=0)
    return df
    
def save_course_csv(updated_course_df, output_file):
    """Saves the updated course dataframe as a .csv file. 
    
    Parameters
    ----------
    updated_course_df : DataFrame 
        A pandas dataframe containing the updated grades for the course.
    output_file: str 
        Path to the output .csv file as a string. 
    
    Returns
    -------
    None
    
    Examples
    --------
    >>> save_course_csv(DSCI100_df, 'DSCI100.csv')
    """
    
    updated_course_df.to_csv(output_file)
    return 

def update_assignment_grade(input_file, assignment, grade):
    """Updates the 'grade' column of 'course.csv' with the new grade inputted. Can add a grade if there was no grade for the assignment previously, or change the current grade of the assignment to a new one. Will call 'save_course_csv' to save the updated dataframe as 'course.csv'. 
    
    Parameters
    ----------
    input_file : str
        Path to the .csv file as a string. 
    assignment: str
        Name of the assignment to be updated as a string. 
    grade : double 
        Grade of the assignment as a double. 
    
    Returns
    -------
    None
    
    Examples
    --------
    >>> update_assignment_grade('DSCI100.csv', 'Assignment 1', 95.0)
    """
    
    df = load_course(input_file)          # load_course() has its own exceptions 
    row = df['Components'] == assignment    # find the row number with the assignment 
    df.loc[row, 'Grades (%)'] = round(grade, 2)     # update grade and round 
    save_course_csv(df, input_file)       # save course as .csv into original input_file location 
                                          # save_course_csv() has its own exceptions
        
    
