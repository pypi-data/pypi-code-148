



def calculate_grade(grade,credits):
    if grade >=95:
        letter_grade = "A+"
        weighted_grade = 5.0
        points=credits*weighted_grade
    elif grade >=90:
        letter_grade = "A"
        weighted_grade = 4.75
        points=credits*weighted_grade
    elif grade >=85:
        letter_grade = "B+"
        weighted_grade = 4.5
        points=credits*weighted_grade
    elif grade >=80:
        letter_grade = "B"
        weighted_grade = 4.0
        points=credits*weighted_grade
    elif grade >=75:
        letter_grade = "C+"
        weighted_grade = 3.5
        points=credits*weighted_grade
    elif grade >=70:
        letter_grade = "C"
        weighted_grade = 3.0
        points=credits*weighted_grade
    elif grade >=65:
        letter_grade = "D+"
        weighted_grade = 2.5
        points=credits*weighted_grade
    elif grade >=60:
        letter_grade = "D"
        weighted_grade = 2.0
        points=credits*weighted_grade
    else:
        letter_grade = "F"
        weighted_grade =0.0
        points=credits*weighted_grade
   
    return letter_grade,weighted_grade,points




def calculate_GPA(last_GPA,last_credits,grades_list,credits_list):
    semester_credits=0
    semester_points=0
    str1='Your semster GPA and overall GPA are: '
    counter=0
    
    
    for grade,credits in zip(grades_list,credits_list):
        counter+=1
        letter_grade,weighted_grade,points= calculate_grade(grade,credits)
        print('you got in course',counter,letter_grade,'(',weighted_grade,')',"with total points = ", points)
        semester_credits += credits
        semester_points += points
        last_points=last_GPA*last_credits
        semester_GPA =round((semester_points/ semester_credits),2) 
        overall_credits=last_credits+semester_credits
        overall_points=last_points+semester_points
        overall_GPA=round((overall_points/overall_credits),2)
        
        
    return str1,semester_GPA,overall_GPA
 


