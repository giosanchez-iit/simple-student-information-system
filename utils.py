from PyQt5.QtCore import QObject, pyqtSignal
from functools import partial
import os
import csv
import re

    
class Utils(QObject):
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    # CRUDL implementations for the STUDENT data
        
    def studentCreate(id_num, student_name, yr_level, gender, course_code):
        # Check if the file exists and is not empty
        file_exists = os.path.isfile('students.csv')
        file_empty = not file_exists or os.stat('students.csv').st_size == 0

        # Read the file content if it's not empty
        if not file_empty:
            with open('students.csv', 'r', newline='') as csvfile:
                content = csvfile.read()

            # Check if the last character is not a newline
            if content[-1] != '\n':
                content += '\n'  # Append a newline

            # Write the modified content back to the file
            with open('students.csv', 'w', newline='') as csvfile:
                csvfile.write(content)

        # Open the file in append mode and write the new student information
        with open('students.csv', 'a', newline='') as csvfile:
            fieldnames = ['ID Number', 'Name', 'Year Level', 'Gender', 'Course Code', 'Enrollment Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write headers if the file doesn't exist
            if not file_exists:
                writer.writeheader()

            # Set enrollment status based on whether or not "course code" is filled in
            status = 'Not Enrolled' if not course_code else 'Enrolled'

            # Write student information to students.csv
            writer.writerow({'ID Number': id_num,
                            'Name': student_name,
                            'Year Level': yr_level,
                            'Gender': gender,
                            'Course Code': course_code,
                            'Enrollment Status': status})

    def studentRead(row_num):
            with open('students.csv', 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)
                if 0 < row_num <= len(rows):
                    return rows[row_num - 1]  # header is at row_num 1, data starts from row_num 2.
                else:
                    return None

    def studentUpdate(id_num, student_name, yr_level, gender, course_code):
        # Search for row based on id number
        row_num = Utils.studentFind(id_num)
        file_path = 'students.csv'

        # Read the CSV file
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        # Update given info on row of student
        if 0 < row_num <= len(rows):
            # Determine the enrollment status based on whether course_code is empty
            enrollment_status = "Enrolled" if course_code else "Not Enrolled"
            # Update the student information
            rows[row_num - 1][1:] = [student_name, yr_level, gender, course_code, enrollment_status]
            # Write the updated rows back to the CSV file
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            return True
        else:
            return False

    def studentDelete(id_num):
        file_path = 'students.csv'
        try:
            #search for row based on id number
            row_number = Utils.studentFind(id_num)
            with open(file_path, 'r', newline='') as csvfile:
                rows = list(csv.reader(csvfile))
            
            #delete line given info of row number
            del rows[row_number - 1]

            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(rows)
            
            return True
        except Exception as e:
            print(e)
            return False                    


    # Helper functions for the Student CRUDL Implementations

    def studentFind(id_num):
        file_path = 'students.csv'
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if str(row[0]) == id_num:
                    return i + 1  # Adjusting for 1-based indexing
        raise Exception(f"Student with ID number {id_num} not found.")

    def studentValidate(id_num, student_name, yr_level, gender):
            # Check if any of the required fields are blank
            if not (id_num and student_name and yr_level and gender):
                return False
            
            # Check if id_num is in the format ####-####
            if not re.match(r'\d{4}-\d{4}', id_num):
                return False
            
            # If all conditions met, return True
            return True
        
        
    # CRUDL implementations for the COURSE data

    def courseCreate(course_code, course_description):
        # Check if the file exists and is not empty
        file_exists = os.path.isfile('courses.csv')
        file_empty = not file_exists or os.stat('courses.csv').st_size == 0
        
        with open('courses.csv', 'a', newline='') as csvfile:
            # Prepend a newline if the file is not empty and the last character is not a newline
            if not file_empty:
                csvfile.seek(-1, os.SEEK_END)  # Move cursor to the end of the file
                last_char = csvfile.read(1)
                if last_char != '\n':
                    csvfile.write('\n')
            
            fieldnames = ['Course Code', 'Course Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # write headers if courses.csv is empty
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({'Course Code': course_code, 'Course Description': course_description})


    def courseRead(row_num):
        with open('courses.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if 0 < row_num <= len(rows):
                return rows[row_num - 1]
            else:
                return None

    def courseUpdate(course_code, new_course_description):
        with open('courses.csv', 'r', newline='') as csvfile:
            rows = list(csv.DictReader(csvfile))

        for row in rows:
            if row['Course Code'] == course_code:
                row['Course Description'] = new_course_description

        with open('courses.csv', 'w', newline='') as csvfile:
            fieldnames = ['Course Code', 'Course Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return True

    def courseDelete(course_code):
        try:
            with open('courses.csv', 'r', newline='') as csvfile:
                rows = list(csv.DictReader(csvfile))

            new_rows = [row for row in rows if row['Course Code'] != course_code]

            with open('courses.csv', 'w', newline='') as csvfile:
                fieldnames = ['Course Code', 'Course Description']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(new_rows)
            return True
        except Exception as e:
            print(e)
            return False

    def courseList(combo_box, file_path):
        # Read data from CSV file and populate combo box
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                course_code = row[0]
                course_description = row[1]
                combo_box.addItem(f"{course_code} - {course_description}")


    # Helper functions for the Student CRUDL Implementations

    def studentFind(id_num):
        file_path = 'students.csv'
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if str(row[0]) == id_num:
                    return i + 1  # Adjusting for 1-based indexing
        raise Exception(f"Student with ID number {id_num} not found.")

    def studentValidate(id_num, student_name, yr_level, gender):
            # Check if any of the required fields are blank
            if not (id_num and student_name and yr_level and gender):
                return False
            
            # Check if id_num is in the format ####-####
            if not re.match(r'\d{4}-\d{4}', id_num):
                return False
            
            # If all conditions met, return True
            return True
        
    # CRUDL implementations for the COURSE data

    def courseCreate(course_code, course_description):
        with open('courses.csv', 'a', newline='') as csvfile:
            fieldnames = ['Course Code', 'Course Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # write headers if courses.csv is empty
            if csvfile.tell() == 0:
                writer.writeheader()
            
            writer.writerow({'Course Code': course_code, 'Course Description': course_description})

    def courseRead(row_num):
        with open('courses.csv', 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            if 0 < row_num <= len(rows):
                return rows[row_num - 1]
            else:
                return None

    def courseUpdate(course_code, new_course_description):
        with open('courses.csv', 'r', newline='') as csvfile:
            rows = list(csv.DictReader(csvfile))

        for row in rows:
            if row['Course Code'] == course_code:
                row['Course Description'] = new_course_description

        with open('courses.csv', 'w', newline='') as csvfile:
            fieldnames = ['Course Code', 'Course Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        return True

    def courseDelete(course_code):
        try:
            # Read all rows from the CSV file
            with open('students.csv', 'r', newline='') as student_file:
                students = list(csv.DictReader(student_file))

            # Update the enrollment status for all students with the given course code
            for student in students:
                if student['Course Code'] == course_code:
                    student['Course Code'] = ''
                    student['Enrollment Status'] = 'Not Enrolled'

            # Write the modified student data back to the CSV file
            with open('students.csv', 'w', newline='') as student_file:
                fieldnames = ['ID Number', 'Name', 'Year Level', 'Gender', 'Course Code', 'Enrollment Status']
                writer = csv.DictWriter(student_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)

            # Remove the course from the courses.csv file
            with open('courses.csv', 'r', newline='') as course_file:
                courses = list(csv.DictReader(course_file))

            # Filter out the course with the given course code
            new_courses = [course for course in courses if course['Course Code'] != course_code]

            # Write the updated course data back to the CSV file
            with open('courses.csv', 'w', newline='') as course_file:
                fieldnames = ['Course Code', 'Course Description']
                writer = csv.DictWriter(course_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(new_courses)

            return True
        except Exception as e:
            print(e)
            return False


    def courseList(combo_box, file_path):
        # Read data from CSV file and populate combo box
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                course_code = row[0]
                course_description = row[1]
                combo_box.addItem(f"{course_code} - {course_description}")
                
    def courseFind(course_code):
        file_path = 'courses.csv'
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if str(row[0]) == course_code:
                    return i + 1  # Adjusting for 1-based indexing
        raise Exception(f"Course with Course Code {course_code} not found.")