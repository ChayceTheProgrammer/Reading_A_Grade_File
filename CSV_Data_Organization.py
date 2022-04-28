
"""
File:    CSV_Data_Organization.py
Author:  Chayce Leonard (231009015)
Date:    05/09/2022
Email:   chayce4school@tamu.edu
"""

import csv
import os
import matplotlib.pyplot as plt
import statistics as stat
import math

"""
Function which will allow input from the user
"""
def select_option():
    """
    Function that asks user for input of what option from the menu the user wants
    """
    option = -1 # Starts the users choice as -1 as a "null-choice" which means they have not chosen a choice yet
    library_of_grades = {}  # dictionary that will hold every student and their grades as a list
    while option != 6:
        print_menu() # prints menu
        option = int(input("Select from the options above: ")) # asks user for option
        if   option == 1:
            # option for reading grades.csv and obtaining all data for calculations
            all_file_data = get_file_data("Original_Data/grades.csv")[0]

            for line in all_file_data[0:]:
                uin = line[0]                        # UIN is the first element of every row and will the key for the dictionary

                grades_as_list_of_strings = line[1:] # Grades come as strings and are every element after UIN
                grades = [float(grade) for grade in grades_as_list_of_strings] # List comprehension so every number string is converted to a value that allows math to be done to it                     # Grades will be the value for the dictionary

                student = {uin:grades}
                library_of_grades.update(student)
            print("File: \"grades.csv\" has been read!")
            print("")
        elif option == 2:
            if len(library_of_grades) == 0:
                # Case for if file has not been read yet
                print("No file read\n")
                pass
            else:
                generate_student_report_file(library_of_grades)
                print("")
                pass
        elif option == 3:
            if len(library_of_grades) == 0:
                # Case for if grades.csv file has not been read yet
                print("No file read\n")
                pass
            else:
                generate_student_report_charts(library_of_grades)
                print("")
                pass
        elif option == 4:
            if len(library_of_grades) == 0:
                # Case for if file has not been read yet
                print("No file read\n")
                pass
            else:
                generate_class_report(library_of_grades)
                print("")
                pass
        elif option == 5:
            if len(library_of_grades) == 0:
                # Case for if file has not been read yet
                print("No file read\n")
                pass
            else:
                generate_report_charts_for_class(library_of_grades)
                print("")
                pass
        elif option == 6:
            # Case for if user wants to quit
            print("")
            break
        else:
            print("Unexpected Option Choice. Try Again\n")

    print("You have exited the program!")

"""
Next Function which prints the menu
"""
def print_menu():
    """
    Function that simply prints the menu
    """
    print("""*******************Main Menu*****************
1. Read CSV file of grades
2. Generate student report file
3. Generate student report charts
4. Generate class report file
5. Generate class report charts
6. Quit
************************************************
    """)

"""
Function which reads the grades file and obtains the data into a information structure
"""
def get_file_data(file_name):
    """

    Function that opens the file titles grades.csv

    Parameter1: file_name is the name of the file that contains the data
    """
    grades_file = open(file_name)

    # cvs.reader() reads the file line by line
    reading_file = csv.reader(grades_file)

    header_line = next(reading_file)

    every_row = []
    for row in reading_file:
        # Collects all data from every row, except first, in the file into a list and appends that list to the entire data list of every_row
        every_row.append(row)

    # .close() method closes the file
    grades_file.close()
    return every_row, header_line

"""
The Next 8 functions are used for option 2 of the select_option() function which create a file of a 
single student's grades
"""
def generate_student_report_file(dict_of_grades):
    """

    Generates the file which the user is prompted for an uin and writes to a new file titles the uin.txt

    Parameter1: Dictionary of Keys (UINs) and Values (Grades)
    """
    what_uin = input("Enter the specified UIN for the report: ")
    if what_uin not in dict_of_grades.keys():
        # case for if uin entered is not a key in the dictionary specified, then a message pops up and a re-prompt occurs
        print("Invalid UIN")
        generate_student_report_file(dict_of_grades)
    else:
        # Branch that actually calculates the averages and writes to a file
        lab_average     = calculate_everything_single_student(what_uin, dict_of_grades)[0]
        exam_average    = calculate_everything_single_student(what_uin, dict_of_grades)[1]
        quiz_average    = calculate_everything_single_student(what_uin, dict_of_grades)[2]
        reading_average = calculate_everything_single_student(what_uin, dict_of_grades)[3]
        weighted_score  = calculate_everything_single_student(what_uin, dict_of_grades)[4]
        letter          = letter_grade(weighted_score)

        student_report_file = open(f"{what_uin}.txt", "w") # creates empty file titled the UIN specified.txt, in the mode of writing
        print(f"File: \"{what_uin}.txt\" has been created!")
        student_report_file.write(f"Exams mean: {exam_average}\n"
                                  f"Labs mean: {lab_average}\n"
                                  f"Quizzes mean: {quiz_average}\n"
                                  f"Reading activities mean: {reading_average}\n"
                                  f"Score: {weighted_score}%\n"
                                  f"Letter grade: {letter}")
        student_report_file.close()
        print(f"File: \"{what_uin}.txt\" has been updated!")
        return lab_average, exam_average, quiz_average, reading_average, weighted_score

def calc_labs(uin, dict_of_grades):
    """

    Function which will calculate the average of the labs

    Parameter1: uin is the specified UIN which where the specified students grades are held

    Parameter2: dict_of_grades is the dictionary that holds every student's grades
    """
    grades = dict_of_grades[uin]
    labs_scores = grades[0:6]
    lab_mean = sum(labs_scores) / len(labs_scores)
    return lab_mean

def calc_exams(uin, dict_of_grades):
    """

    Function that will calculate the average of the exams

    Parameter1: uin is the specified UIN which where the specified students grades are held

    Parameter2: dict_of_grades is the dictionary that holds every student's grades
    """
    grades = dict_of_grades[uin]
    exam_scores = grades[18:21]
    exam_mean = sum(exam_scores) / len(exam_scores)
    return exam_mean

def calc_quizzes(uin, dict_of_grades):
    """

    Function that calculates the average of the quizzes

    Parameter1: uin is the specified UIN which where the specified students grades are held in dict_of_grades

    Parameter2: dict_of_grades is the dictionary that holds every student's grades

    """
    grades = dict_of_grades[uin]
    quiz_scores = grades[6:12]
    quiz_mean = sum(quiz_scores) / len(quiz_scores)
    return quiz_mean

def calc_readings(uin, dict_of_grades):
    """

    Function that calculates the average of the readings

    Parameter1: uin is the specified UIN which where the specified students grades are held in dict_of_grades

    Parameter2: dict_of_grades is the dictionary that holds every student's grades

    """
    grades = dict_of_grades[uin]
    reading_score = grades[12:18]
    reading_mean = sum(reading_score) / len(reading_score)
    return reading_mean

def calc_score(l_ave, e_ave, q_ave, r_ave, proj):
    """

    Function that calculates the weighted score

    Parameter1: l_ave is the average of the labs

    Parameter2: e_ave is the average of the exams

    Parameter3: q_ave is the average of the quiz's

    Parameter4: r_ave is the average of the reading activities

    Parameter5: proj is the project grade (not an average as there is only one project)

    """
    total_score_list = []

    weighed_labs    = l_ave * .25
    total_score_list.append(weighed_labs)

    weighed_quizzes = q_ave * .10
    total_score_list.append(weighed_quizzes)

    weighed_exams   = e_ave * .45
    total_score_list.append(weighed_exams)

    weighed_reading = r_ave * .10
    total_score_list.append(weighed_reading)

    weighed_project = proj * .10
    total_score_list.append(weighed_project)

    total_score = sum(total_score_list)
    return total_score

def letter_grade(weighted_score):
    """

    Function which calculates letter grades by the weighted Grade

    Parameter1: weighted_score is the average score of a single student

    """
    if weighted_score >= 90:
        grade_letter = 'A'
    elif 90 > weighted_score >= 80:
        grade_letter = 'B'
    elif 80 > weighted_score >= 70:
        grade_letter = 'C'
    elif 70 > weighted_score >= 60:
        grade_letter = 'D'
    else:
        grade_letter = 'F'
    return grade_letter

def calculate_everything_single_student(uin, dict_of_grades):
    """
    Function will calculate the average of all assignment types in a single function

    Parameter1: uin is where the specified student uin will go

    Parameter2: dict_of_grades is what holds every student's grades attached by UIN

    """
    lab_average = round(calc_labs(uin, dict_of_grades), 1)
    exam_average = round(calc_exams(uin, dict_of_grades), 1)
    quiz_average = round(calc_quizzes(uin, dict_of_grades), 1)
    reading_average = round(calc_readings(uin, dict_of_grades), 1)
    project = dict_of_grades[uin][-1]
    weighted_score = round(calc_score(lab_average, exam_average, quiz_average, reading_average, project), 1)
    letter = letter_grade(weighted_score)
    return lab_average, exam_average, quiz_average, reading_average, weighted_score, letter

"""
The Next 6 functions are for option 3 of the select_option() function which creates a directory named their UIN to 
store the 4 bar charts of the different assignment types for a single student
"""
def generate_student_report_charts(dict_of_grades):
    """

    Function that generates both the Bar and Pie Chart for the Letter Grade Distribution

    Parameter1: dict_of_grades is what holds all student's grades attached by UIN

    """
    what_uin = input("Enter the Specified UIN for the chart report: ")
    if what_uin not in dict_of_grades.keys():
        # Branch for the case where uin entered is not in the grades file
        print("Invalid UIN!")
        generate_student_report_charts(dict_of_grades)
    else:
        # Branch that actually creates the bar charts for the individual
        path = create_directory(what_uin)

        header_line = (get_file_data("Original_Data/grades.csv"))[1]
        student_grades = dict_of_grades[what_uin]

        generate_labs_bar_chart(student_grades, header_line, what_uin, path)
        generate_exams_bar_chart(student_grades, header_line, what_uin, path)
        generate_readings_bar_chart(student_grades, header_line, what_uin, path)
        generate_quiz_bar_chart(student_grades, header_line, what_uin, path)

def create_directory(directory_name):
    """

    Function Creates a directory with the name provided which will hold Charts

    Parameter1: directory_name is the desired directory name

    """
    new_directory = f"/{directory_name}"
    '''parent_directory = "C:/Users/Public/PycharmProjects/Project[CSCE110]"'''
    parent_directory = "."
    path = parent_directory + new_directory
    os.mkdir(path, mode=0o666)
    print(f"Directory named \"{directory_name}\" at path: \"{path}\" was created!\n"
          f"Check Your FILES!")
    return path

def generate_labs_bar_chart(student_grades, header_line, uin, save_path):
    """

    Function that creates the bar chart for labs

    Parameter1: student_grades is the section of the dictionary that has the specified student's grades

    Parameter2: header_line is the line on top of the grades.csv file which depicts what grades mean what

    Parameter3: uin is the current student's UIN

    Parameter4: save_path is for the chart to be saved at the newly created directory, *******action needed******

    """
    lab_scores = student_grades[0:6]
    each_lab = header_line[1:7]
    plt.figure(1)
    plt.bar(each_lab, lab_scores, color="red", width=.5)
    plt.xlabel("Lab Assignments")
    plt.ylabel("Score")
    plt.title(f"Grades for Lab Assignments for the student with UIN: {uin}")
    plt.savefig(save_path + f"/{uin}_Lab_Bar_Chart.png")

def generate_exams_bar_chart(student_grades, header_line, uin, save_path):
    """

    Function that creates the bar chart for the exams

    Parameter1: student_grades is the section of the dictionary that has the specified student's grades

    Parameter2: header_line is the line on top of the grades.csv file which depicts what grades mean what

    Parameter3: uin is the current student's UIN

    Parameter4: save_path is for the chart to be saved at the newly created directory, *******action needed******

    """
    exam_scores = student_grades[18:21]
    each_exam = header_line[19:22]
    plt.figure(2)
    plt.bar(each_exam, exam_scores, color="red", width=.5)
    plt.xlabel("Exam Number")
    plt.ylabel("Score")
    plt.title(f"Grades for Exams for Student with UIN: {uin}")
    plt.savefig(save_path + f"/{uin}_Exam_Bar_Chart.png")

def generate_readings_bar_chart(student_grades, header_line, uin, save_path):
    """

    Function that creates the bar chart for reading activities

    Parameter1: student_grades is the section of the dictionary that has the specified student's grades

    Parameter2: header_line is the line on top of the grades.csv file which depicts what grades mean what

    Parameter3: uin is the current student's UIN

    Parameter4: save_path is for the chart to be saved at the newly created directory, *******action needed******

    """
    reading_scores = student_grades[12:18]
    each_reading = header_line[13:19]
    plt.figure(3)
    plt.bar(each_reading, reading_scores, color="red", width=.5)
    plt.xlabel("Reading Assignment")
    plt.ylabel("Score")
    plt.title(f"Grades for Reading Assignments for Student with UIN: {uin}")
    plt.savefig(save_path + f"/{uin}_Readings_Bar_Chart.png")

def generate_quiz_bar_chart(student_grades, header_line, uin, save_path):
    """

    Function that creates the bar chart for all the quiz's

    Parameter1: student_grades is the section of the dictionary that has the specified student's grades

    Parameter2: header_line is the line on top of the grades.csv file which depicts what grades mean what

    Parameter3: uin is the current student's UIN

    Parameter4: save_path is for the chart to be saved at the newly created directory, *******action needed******

    """
    quiz_scores = student_grades[6:12]
    each_quiz = header_line[7:13]
    plt.figure(4)
    plt.bar(each_quiz, quiz_scores, color="red", width=.5)
    plt.xlabel("Quiz Number")
    plt.ylabel("Score")
    plt.title(f"Grades for Quiz Assignments for Student with UIN: {uin}")
    plt.savefig(save_path + f"/{uin}_Quiz_Bar_Chart.png")

"""
These Next 7 Functions are specifically for option 4 of the select_option() function
Some of these functions have functions that were used for option 2 of select_option() function
"""
def generate_class_report(dict_of_grades):
    """

    Option for instructor to get data about the entire class

    Parameter1: Dictionary that holds every student's uin and grades

    """
    total_students = len(list(dict_of_grades.keys()))
    minimum_score  = lowest_class_score(dict_of_grades)
    maximum_score  = highest_class_score(dict_of_grades)
    median_score   = class_median_score(dict_of_grades)
    average_score  = class_average_score(dict_of_grades)
    standard_dev   = class_standard_dev(dict_of_grades)

    class_report_file = open(f"report.txt", "w") # Creates empty file for the report
    class_report_file.write(f"Total number of students: {total_students}\n"
                            f"Minimum score: {minimum_score}\n"
                            f"Maximum score: {maximum_score}\n"
                            f"Median score: {median_score}\n"
                            f"Mean score: {average_score}\n"
                            f"Standard deviation: {standard_dev}\n"
                            )
    print(f"Class Report Generated!")
    print(f"Check files for the report!")

def find_all_student_scores(dict_of_grades):
    """

    Function which calculates every student's weighted score

    Parameter1: Dictionary that holds all students UIN and respective grades

    """
    scores = []
    for key in dict_of_grades:
        score = calculate_everything_single_student(key, dict_of_grades)[4]
        scores.append(score)

    return scores

def lowest_class_score(dict_of_grades):
    """

    Function which finds the lowest weighted score for the report of the class

    Parameter1: Dictionary that holds all students uin and respective grades
    """
    lowest_score = min(find_all_student_scores(dict_of_grades))
    return lowest_score

def highest_class_score(dict_of_grades):
    """

    Function which finds the highest weighted score for the report of the class

    Parameter1: Dictionary that holds all students uin and respective grades

    """
    highest_score = max(find_all_student_scores(dict_of_grades))
    return highest_score

def normal_rounding(number, decimal_places):
    """

    round() function always rounds to the nearest even number, this function will
    allow you to round any number to a specified number of decimal places traditionally
    instead of "banker's rounding" of rounding to the nearest even number

    Parameter1: number The Number you want to round to

    Parameter2: decimal_places How many decimal places you want to round

    """
    exponent = number * 10 ** decimal_places
    if abs(exponent) - abs(math.floor(exponent)) < .5:
        return math.floor(exponent) / 10 ** decimal_places
    else:
        return math.ceil(exponent) / 10 ** decimal_places

def class_median_score(dict_of_grades):
    """

    Function that finds the median of all scores of the class

    Parameter1: dictionary of grades that holds UIN and grades

    """
    median = normal_rounding(stat.median(find_all_student_scores(dict_of_grades)), 1)
    return median

def class_average_score(dict_of_grades):
    """

    Function which finds the average of the class

    parameter1: Dictionary of UINs and respective grades

    """
    class_average = round((sum(find_all_student_scores(dict_of_grades)) / len(find_all_student_scores(dict_of_grades))), 1)
    return class_average

def class_standard_dev(dict_of_grades):
    """

    Function that finds the standard deviation of the entire class's weighed scores

    Parameter1: Dictionary of {UINs:[Grades]}

    """
    grades = find_all_student_scores(dict_of_grades)
    standard_dev = round(stat.stdev(grades), 1)
    return standard_dev

"""
The next 5 functions are used for option 5 of the program and will be used to make a Pie Chart
and a Bar Chart of Letter Grades of the class
"""
def generate_report_charts_for_class(dict_of_grades):
    """

    Function which will generate the actual charts (pie and bar) for the class

    Parameter1: dict_of_grades holds all student data {UIN:[grades]}

    """
    directory_name = "class_charts"
    created_directory = create_directory(directory_name)
    all_letter_grades = get_all_letter_grades(dict_of_grades)
    distribution = letter_grade_distribution(all_letter_grades)

    generate_class_letter_grades_pie_chart(distribution, created_directory)
    generate_class_letter_grades_bar_chart(distribution, created_directory)

def get_all_letter_grades(dict_of_grades):
    """

    Function which finds the letter grade of every student in the class

    Parameter1: dict_of_grades holds all students UINs and their respective grades

    """
    letter_grades = []
    for key in dict_of_grades:
        letter = calculate_everything_single_student(key, dict_of_grades)[5]
        letter_grades.append(letter)
    return letter_grades

def letter_grade_distribution(list_of_letter_grades):
    """

    Function which finds the Distribution of all the letter grades of the class

    Parameter1: list_of_letter_grades is just a list that holds every student's letter grade in order of UIN in
    "grades.csv" file

    """
    letter_distribution = {}
    for letter in list_of_letter_grades:
        if letter in letter_distribution:
            letter_distribution[letter] += 1
        if letter not in letter_distribution:
            key = letter
            value = 1
            item = {key:value}
            letter_distribution.update(item)
    return letter_distribution

def generate_class_letter_grades_pie_chart(dict_of_letter_occurances, save_path):
    """

    Function which actually generates a pie chart of the letter grade distribution

    Parameter1: dict_of_letter_occurances holds each letter grade as a key and the number of times the grade shows up
    as the value

    """
    data = dict_of_letter_occurances.values()
    grade_distribution_labels = dict_of_letter_occurances.keys()
    plt.figure(5)
    plt.pie(data, labels=grade_distribution_labels, autopct='%1.1f%%')
    plt.title("Class Letter Grade Distribution")
    plt.axis("equal")
    plt.savefig(save_path + f"/Class_Letter_Distribution_Pie_Chart.png")

    print("Class Letter Grade Distribution Pie Chart Generated!")
    print("Check your files!")


def generate_class_letter_grades_bar_chart(dict_of_letter_occurances, save_path):
    """

    Function which actually generates the bar chart of the letter grade distribution

    Parameter1: dict_of_letter_occurances holds each letter grade as a key and the number of times the grade shows up
    as a value
    """
    data = dict_of_letter_occurances.values()
    labels = dict_of_letter_occurances.keys()
    plt.figure(6)
    plt.bar(labels, data, color="red", width=.5)
    plt.xlabel("Letter Grades")
    plt.ylabel("Distribution")
    plt.title("Distribution of Letter Grades")
    plt.savefig(save_path + "/Class_Letter_Grade_Distribution_Bar_Chart.png")
    print("Class Letter Grade Distribution Bar Chart Generated!")
    print("Check Your Files!")

"""
Main Driver Function
"""
def main():
    """Driver Function that calls all other functions"""
    select_option()

main()