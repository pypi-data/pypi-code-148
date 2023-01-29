import pandas as pd
import os

def construct_course(course_name, output_file_path):
    """
    Allow user to input course components' information (component name and coresponding weight) one by one.
    Course components could be the following for example:
    1. Assignment(s)
    2. Quiz(s)
    3. Lab(s)
    4. Midterm(s)
    5. Final(s)
    6. Any user self-defined course component name(s)

    Save the course information as a .csv file (named based on the 'course_name' paramater) 
    to the file path specified by 'output_file_path' paramater
    
    Parameters
    ----------
    course_name: str 
        The course name as a string. It will be used as the output file name 

    output_file_path: str 
        Path to the output .csv file (named based on the 'course_name' paramater) 
        under the current working directory as a string. 
        The purpose to save under the current working directory it to avoid permission issue.
    
    Returns
    -------
    None

    Examples
    --------
    >>> construct_course('dsci524', '/')
    """
    
    course_total_weight = 0
    course_df = pd.DataFrame(columns = ["Components", "Weights (%)", "Grades (%)"])
    index = 0

    while course_total_weight < 100:
        curr_component = []

        curr_component_name = input(f"What is name of {course_name} component #{index+1}? ")

        # Check if the weight input can be parsed as integer
        curr_component_weight_input = input(f"What is weight(%) of {course_name} component #{index+1}? ")
        while not curr_component_weight_input.isdigit():
            curr_component_weight_input = input(f"Input weight(%) of {course_name} component #{index+1} as integer? ")

        curr_component_weight = int(curr_component_weight_input)

        # Check if the total weight not over 100%
        while course_total_weight + curr_component_weight > 100:
            curr_component_weight = int(input(f"Double check the weight of {course_name} component #{index+1}, ensure total weight not over 100%? "))

        curr_component.append(curr_component_name)
        curr_component.append(curr_component_weight)
        curr_component.append(float('nan'))

        course_df.loc[index] = curr_component

        course_total_weight += curr_component_weight

        index += 1

    # save course construction dataframe as csv file
    cwd = os.getcwd()
    path = cwd + output_file_path
    filepath = os.path.join(path, course_name + ".csv")
    course_df.to_csv(filepath)

    print(course_df)