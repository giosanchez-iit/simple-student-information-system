import csv
from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
from gui_course import *
from gui_student import *
from utils import Utils


class Ui_mainWindow(object):

    def setupUi(self, mainWindow):
        
        # Declare our Popups
        
        self.ui_course_popup = CoursePopup()
        self.ui_student_popup = StudentPopup()
        self.utils_instance = Utils()
        
        # Graphics Interface Setup
        
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1000, 700)
        
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.courseSelectComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.courseSelectComboBox.setGeometry(QtCore.QRect(110, 20, 421, 22))
        self.courseSelectComboBox.setObjectName("courseSelectComboBox")
        
        self.selectCourseLabel = QtWidgets.QLabel(self.centralwidget)
        self.selectCourseLabel.setGeometry(QtCore.QRect(30, 20, 101, 21))
        self.selectCourseLabel.setObjectName("selectCourseLabel")
        
        self.courseCreate = QtWidgets.QPushButton(self.centralwidget)
        self.courseCreate.setGeometry(QtCore.QRect(540, 20, 131, 23))
        self.courseCreate.setObjectName("courseCreate")
        
        self.courseUpdate = QtWidgets.QPushButton(self.centralwidget)
        self.courseUpdate.setGeometry(QtCore.QRect(710, 20, 121, 23))
        self.courseUpdate.setStyleSheet("background-color:rgb(251, 141, 26);\n"
        "color:rgb(255, 255, 255);")
        self.courseUpdate.setObjectName("courseUpdate")
        
        self.courseDelete = QtWidgets.QPushButton(self.centralwidget)
        self.courseDelete.setGeometry(QtCore.QRect(840, 20, 121, 23))
        self.courseDelete.setStyleSheet("background-color:rgb(232, 8, 62); color:rgb(255, 255, 255);")
        self.courseDelete.setObjectName("courseDelete")
        
        self.studentCreate = QtWidgets.QPushButton(self.centralwidget)
        self.studentCreate.setGeometry(QtCore.QRect(460, 650, 111, 23))
        self.studentCreate.setStyleSheet("background-color:  #02864a; color: #fff;")
        self.studentCreate.setObjectName("studentCreate")
        
        self.studentListTable = QtWidgets.QTableWidget(self.centralwidget)
        self.studentListTable.setGeometry(QtCore.QRect(35, 70, 931, 561))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.studentListTable.sizePolicy().hasHeightForWidth())
        
        self.studentListTable.setSizePolicy(sizePolicy)
        self.studentListTable.setStyleSheet("QTableWidget{\n"
        "    selection-color: #fff;\n"
        "    selection-background-color: #573CFA;\n"
        "}\n"
        "\n"
        "QHeaderView{\n"
        "    background-color: #02864a;\n"
        "    color: #fff;\n"
        "}\n"
        "\n"
        "QHeaderView::section{\n"
        "    background-color:  #02864a;\n"
        "    color: #fff;\n"
        "}")
        
        self.studentListTable.setObjectName("studentListTable")
        self.studentListTable.setColumnCount(8)
        self.studentListTable.setRowCount(0)
        # Set headers
        self.studentListTable.setHorizontalHeaderLabels(["ID Number", "Name", "Year Level", "Gender", "Course Code", "Enrollment Status", " ", " "])
        # Set column width
        self.studentListTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.studentListTable.setColumnWidth(0, 100)  # Adjust the width as needed for each column
        self.studentListTable.setColumnWidth(1, 290)  # Adjust the width as needed for each column
        self.studentListTable.setColumnWidth(2, 100)  # Adjust the width as needed for each column
        self.studentListTable.setColumnWidth(3, 100)  # Adjust the width as needed for each column
        self.studentListTable.setColumnWidth(4, 100)  # Adjust the width as needed for each column
        self.studentListTable.setColumnWidth(5, 100)  # Adjust the width as needed for each column
        self.studentListTable.setColumnWidth(6, 60)  # Adjust the width as needed for each column
        self.studentListTable.setColumnWidth(7, 60)  # Adjust the width as needed for each column
        # Remove row and column bars
        self.studentListTable.verticalHeader().setVisible(False)
        # Make the data uneditable
        self.studentListTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.studentListTable.setShowGrid(False)
        # Cell borders only on top and bottom
        self.studentListTable.setStyleSheet("""
            QTableView {
                border: 0px;
            }
            QTableView::item {
                border-top: 1px solid black;
            }
        """)
        # Make cells unresizeable
        self.studentListTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.studentListTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.studentListTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.studentListTable.setFocusPolicy(QtCore.Qt.NoFocus)
        
        # Implement Course Buttons Behaviour
        self.courseSelectComboBox.currentIndexChanged.connect(self.update_button_state)
        self.update_button_state()
        
        # More UI Stuff...
        mainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        
        
        # CRUDL Functionality setup 
        # We will need some instances
        utils = Utils()    
        
        
        # Create
        self.courseCreate.clicked.connect(self.open_course_popup)
        self.studentCreate.clicked.connect(self.open_student_popup)
        
        # Update
        self.courseSelectComboBox.currentIndexChanged.connect(self.update_student_table)
        self.courseUpdate.clicked.connect(self.edit_course_popup)
        
        # List
        self.update_course_combo_box();
        self.update_student_table();
        
        # Delete
        self.courseDelete.clicked.connect(self.delete_course_popup)
             
    # Method definitions for setupUI functionality
    
    def open_course_popup(self):
        self.course_popup = QtWidgets.QDialog()
        self.ui_course_popup.setupUi(self.course_popup,  mode = 'create')
        self.course_popup.finished.connect(self.update_course_combo_box)
        self.course_popup.exec_()
    
    def open_student_popup(self):
        self.student_popup = QtWidgets.QDialog()
        self.ui_student_popup.setupUi(self.student_popup, mode='create')
        self.student_popup.finished.connect(self.update_student_table)
        self.student_popup.exec_()
        
    def edit_student_popup(self, id_number):
        student_info = Utils.studentRead(Utils.studentFind(id_number))
        id_number, name, yr_level, gender, course_code = student_info[:5]
        self.student_popup = QtWidgets.QDialog()
        self.ui_student_popup.setupUi(self.student_popup, mode='edit', id_number=id_number, name=name, gender=gender, yr_level=yr_level, course_code=course_code)
        self.student_popup.finished.connect(self.update_student_table)
        self.student_popup.exec_()
        
    def delete_student_popup(self, id_number):
        student_info = Utils.studentRead(Utils.studentFind(id_number))
        id_number, name, yr_level, gender, course_code = student_info[:5]
        self.student_popup = QtWidgets.QDialog()
        self.ui_student_popup.setupUi(self.student_popup, mode='delete', id_number=id_number, name=name, gender=gender, yr_level=yr_level, course_code=course_code)
        self.student_popup.finished.connect(self.update_student_table)
        self.student_popup.exec_()
    
    def edit_course_popup(self):
        selected_course = self.courseSelectComboBox.currentText()
        if selected_course != '- All Students -' and selected_course != '= Not Enrolled =':
            course_code = selected_course.split()[0]
            course_info = Utils.courseRead(Utils.courseFind(course_code))
            course_code, course_description = course_info[:2]
            self.course_popup = QtWidgets.QDialog()
            self.ui_course_popup.setupUi(self.course_popup, mode='edit', course_code=course_code, course_description=course_description)
            self.course_popup.finished.connect(self.update_course_combo_box)
            self.course_popup.exec_()
    
    def delete_course_popup(self):
        selected_course = self.courseSelectComboBox.currentText()
        if selected_course != '- All Students -' and selected_course != '= Not Enrolled =':
            course_code = selected_course.split()[0]
            course_info = Utils.courseRead(Utils.courseFind(course_code))
            course_code, course_description = course_info[:2]
            self.course_popup = QtWidgets.QDialog()
            self.ui_course_popup.setupUi(self.course_popup, mode='delete', course_code=course_code, course_description=course_description)
            self.course_popup.finished.connect(self.update_course_combo_box)
            self.course_popup.exec_()
    
    def update_course_combo_box(self):
        self.courseSelectComboBox.clear()
        self.courseSelectComboBox.addItem("- All Students -")
        self.courseSelectComboBox.addItem("= Not Enrolled =")
        Utils.courseList(self.courseSelectComboBox, "courses.csv")
        
    def update_student_table(self):
        self.studentListTable.clear()
        self.studentListTable.setRowCount(0)
        course = self.courseSelectComboBox.currentText()
        if course != '':
            self.studentList("students.csv", course.split()[0])
    
    # List
    
    def studentList(self, file_path, course_to_display):
        qtable_widget = self.studentListTable  # Get the QTableWidget from the class instance
        qtable_widget.clear()
        # Read data from CSV file and populate QTableWidget
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for row in reader:
                # Check if the course code matches the course to display
                if course_to_display == '=':
                    if row[4] == '' or row[4] == '-':  # Check if course code is blank or '-'
                        self.add_row(qtable_widget, row)
                elif row[4] == course_to_display or course_to_display == '-':
                    self.add_row(qtable_widget, row)

    def add_row(self, qtable_widget, row):
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
        # Connect the 'clicked' signal of the button to the edit_student_popup method of Ui_mainWindow class
        edit_button.clicked.connect(lambda _, id_number=id_number: self.edit_student_popup(id_number))

        qtable_widget.setCellWidget(row_position, 6, edit_button)
        # Add 'delete' button
        delete_button = QPushButton('Delete')
        delete_button.setStyleSheet("background-color:rgb(232, 8, 62); color:rgb(255, 255, 255);")
        delete_button.clicked.connect(lambda _, id_number=id_number: self.delete_student_popup(id_number))
        qtable_widget.setCellWidget(row_position, 7, delete_button)
        # Set Headers (You may want to set headers outside the loop)
        qtable_widget.setHorizontalHeaderLabels(["ID Number", "Name", "Year Level", "Gender", "Course Code", "Enrollment Status", " ", " "])
        
    # Button Behaviour
    def update_button_state(self):
        selected_course = self.courseSelectComboBox.currentText()
        if selected_course == '- All Students -' or selected_course == '= Not Enrolled =':
            self.courseUpdate.setStyleSheet("background-color: gray; color: #fff;")
            self.courseDelete.setStyleSheet("background-color: gray; color: #fff;")
            self.courseUpdate.setEnabled(False)
            self.courseDelete.setEnabled(False)
        else:
            self.courseUpdate.setStyleSheet("background-color: #FB8D1A; color: #fff;")
            self.courseDelete.setStyleSheet("background-color: #E8083E; color: #fff;")
            self.courseUpdate.setEnabled(True)
            self.courseDelete.setEnabled(True)
               
    # Retranslate elements in setupUI
    
    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "MainWindow"))
        self.selectCourseLabel.setText(_translate("mainWindow", "Select Course:"))
        self.courseCreate.setText(_translate("mainWindow", "Add New Course"))
        self.courseDelete.setText(_translate("mainWindow", "Delete This Course"))
        self.studentCreate.setText(_translate("mainWindow", "Add New Student"))
        item = self.studentListTable.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "ID Number"))
        item = self.studentListTable.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "Name"))
        item = self.studentListTable.horizontalHeaderItem(2)
        item.setText(_translate("mainWindow", "Year Level"))
        item = self.studentListTable.horizontalHeaderItem(3)
        item.setText(_translate("mainWindow", "Gender"))
        item = self.studentListTable.horizontalHeaderItem(4)
        item.setText(_translate("mainWindow", "Enrollment Status"))
        item = self.studentListTable.horizontalHeaderItem(5)
        item.setText(_translate("mainWindow", "Edit"))
        item = self.studentListTable.horizontalHeaderItem(6)
        item.setText(_translate("mainWindow", "Delete"))
        self.courseUpdate.setText(_translate("mainWindow", "Edit This Course"))
        
    def closeEvent(self, event):
        # Emit the 'closed' signal when the dialog is closed
        self.closed.emit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
