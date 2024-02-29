from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
from PyQt5.QtCore import QObject, pyqtSignal

import csv
import re

    
class Utils(QObject):
    
    # emit signal to edit student
    edit_student_signal = pyqtSignal(str)
    
    # CRUDL implementations for the STUDENT data
    
    def studentCreate(id_num, student_name, yr_level, gender, course_code):
        with open('students.csv', 'a', newline='') as csvfile:
            fieldnames = ['ID Number', 'Name', 'Year Level', 'Gender', 'Course Code', 'Enrollment Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # write headers if students.csv is empty
            if csvfile.tell() == 0:
                writer.writeheader()
            
            # set enrollment status based on whether or not "course code" is filled in.
            if course_code == '':
                status = 'Not Enrolled'
            else:
                status = 'Enrolled'
                
            # write student information to students.csv
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
        #search for row based on id number
        row_num = super.studentFind(id_num)
        file_path = 'students.csv'
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

        #update given info on row of student
        if 0 < row_num <= len(rows):
            rows[row_num - 1][1:] = [student_name, yr_level, gender, course_code]  # start from the 2nd column (index 1)
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
            row_number = super.studentFind(id_num)
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

    @staticmethod
    def studentList(qtable_widget, file_path, course_to_display):
        qtable_widget.clear()
        # Read data from CSV file and populate QTableWidget
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                # Check if the course code matches the course to display
                if row[4] == course_to_display or course_to_display == '-':
                    # Insert a new row
                    row_position = qtable_widget.rowCount()
                    qtable_widget.insertRow(row_position)
                    # Populate columns
                    for column, value in enumerate(row):  # Include all columns
                        item = QTableWidgetItem(value)
                        qtable_widget.setItem(row_position, column, item)
                    # Add 'edit' button
                    edit_button = QPushButton('Edit')
                    edit_button.setStyleSheet("background-color:rgb(251, 141, 26); color:rgb(255, 255, 255);")
                    id_number = row[0]
                    # Emit the ID number using the signal
                    utils_instance = Utils()
                    edit_button.clicked.connect(lambda _, id=id_number: Utils.emit_edit_student_signal(id))
                    qtable_widget.setCellWidget(row_position, 6, edit_button)
                    # Add 'delete' button
                    delete_button = QPushButton('Delete')
                    delete_button.setStyleSheet("background-color:rgb(232, 8, 62); color:rgb(255, 255, 255);")
                    qtable_widget.setCellWidget(row_position, 7, delete_button)
                    # Set Headers (You may want to set headers outside the loop)
                    qtable_widget.setHorizontalHeaderLabels(["ID Number", "Name", "Year Level", "Gender", "Course Code", "Enrollment Status", " ", " "])



    # Helper functions for the Student CRUDL Implementations

    def edit_student_handler(id_number):
        pass

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
        
    def editButtonClicked(id_number):
        row_number = super.studentFind(id_number)
        print(row_number)
    
    @staticmethod
    def emit_edit_student_signal(id_number):
        utils_instance = Utils()
        utils_instance.edit_student_signal.emit(id_number)
        
        
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

    def edit_student_handler(id_number):
        pass

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
        
    def editButtonClicked(id_number):
        row_number = super.studentFind(id_number)
        print(row_number)
        
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