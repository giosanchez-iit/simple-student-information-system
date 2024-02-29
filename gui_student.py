from PyQt5 import QtCore, QtGui, QtWidgets
from utils import Utils

class StudentPopup(QtWidgets.QDialog):
    # Define a signal named 'closed'
    
    closed = QtCore.pyqtSignal()
    
    def setupUi(self, MainWindow, mode, id_number=None, name=None, gender=None, yr_level=None, course_code=None):
        
        # Graphics Interface Setup
            
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(279, 250)
            
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
            
        self.student_create = QtWidgets.QPushButton(self.centralwidget)
        self.student_create.setGeometry(QtCore.QRect(90, 200, 111, 23))
        self.student_create.setStyleSheet("background-color: #02864a; color: #fff;")
        self.student_create.setObjectName("student_create")
            
        self.id_num1 = QtWidgets.QLineEdit(self.centralwidget)
        self.id_num1.setGeometry(QtCore.QRect(80, 20, 81, 20))
        self.id_num1.setObjectName("id_num1")
        self.id_num1.setMaxLength(4)
            
        self.id_num2 = QtWidgets.QLineEdit(self.centralwidget)
        self.id_num2.setGeometry(QtCore.QRect(180, 20, 81, 20))
        self.id_num2.setObjectName("id_num2")
        self.id_num2.setMaxLength(4)
            
        self.id_num_label = QtWidgets.QLabel(self.centralwidget)
        self.id_num_label.setGeometry(QtCore.QRect(20, 21, 71, 20))
        self.id_num_label.setObjectName("id_num_label")
            
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(170, 20, 21, 20))
        self.label_2.setObjectName("label_2")
            
        self.name_label = QtWidgets.QLabel(self.centralwidget)
        self.name_label.setGeometry(QtCore.QRect(20, 51, 71, 20))
        self.name_label.setObjectName("name_label")
            
        self.student_name = QtWidgets.QLineEdit(self.centralwidget)
        self.student_name.setGeometry(QtCore.QRect(80, 50, 181, 20))
        self.student_name.setObjectName("student_name")
            
        self.gender_label = QtWidgets.QLabel(self.centralwidget)
        self.gender_label.setGeometry(QtCore.QRect(20, 81, 71, 20))
        self.gender_label.setObjectName("gender_label")
            
        self.enrolled_label = QtWidgets.QLabel(self.centralwidget)
        self.enrolled_label.setGeometry(QtCore.QRect(20, 130, 121, 16))
        self.enrolled_label.setObjectName("enrolled_label")
            
        self.course_select = QtWidgets.QComboBox(self.centralwidget)
        self.course_select.setGeometry(QtCore.QRect(80, 160, 181, 22))
        self.course_select.setObjectName("course_select")
            
        self.enrolled_yes = QtWidgets.QRadioButton(self.centralwidget)
        self.enrolled_yes.setGeometry(QtCore.QRect(180, 130, 41, 17))
        self.enrolled_yes.setObjectName("enrolled_yes")
            
        self.enrolled_no = QtWidgets.QRadioButton(self.centralwidget)
        self.enrolled_no.setGeometry(QtCore.QRect(230, 130, 31, 17))
        self.enrolled_no.setObjectName("enrolled_no")
            
        self.yr_level_label = QtWidgets.QLabel(self.centralwidget)
        self.yr_level_label.setGeometry(QtCore.QRect(150, 80, 61, 21))
        self.yr_level_label.setObjectName("yr_level_label")
            
        self.yr_level = QtWidgets.QComboBox(self.centralwidget)
        self.yr_level.setGeometry(QtCore.QRect(210, 80, 51, 22))
        self.yr_level.setObjectName("yr_level")
            
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(20, 110, 251, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
            
        self.course_select_label = QtWidgets.QLabel(self.centralwidget)
        self.course_select_label.setGeometry(QtCore.QRect(20, 160, 61, 21))
        self.course_select_label.setObjectName("course_select_label")
            
        self.gender = QtWidgets.QComboBox(self.centralwidget)
        self.gender.setGeometry(QtCore.QRect(80, 80, 51, 22))
        self.gender.setObjectName("gender")
            
        # Set Initial States
        
        # adjust fields based on the mode
        if mode == 'create':
            # all fields editable
            self.id_num1.setReadOnly(False)
            self.id_num2.setReadOnly(False)
            self.student_name.setReadOnly(False)
            self.gender.setEnabled(True)
            self.yr_level.setEnabled(True)
            self.course_select.setEnabled(True)
            self.enrolled_yes.setChecked(True)
            self.student_create.setEnabled(False)
            # boxes white to signify non-editable
            self.id_num1.setStyleSheet("background-color: #FFFFFF;")
            self.id_num2.setStyleSheet("background-color: #FFFFFF;")
        elif mode == 'edit':
            # id number fields non-editable
            self.id_num1.setReadOnly(True)
            self.id_num2.setReadOnly(True)
            # boxes gray to signify non-editable
            self.id_num1.setStyleSheet("background-color: #F0F0F0;")
            self.id_num2.setStyleSheet("background-color: #F0F0F0;")
            
            # Fill fields with provided values
            self.id_num1.setText(id_number.split('-')[0])
            self.id_num2.setText(id_number.split('-')[1])
            self.student_name.setText(name)
            self.gender.setCurrentText(gender)
            self.yr_level.setCurrentText(yr_level)
            self.course_select.setCurrentText(course_code)
            
            # Set radio button based on course code
            if course_code:
                self.enrolled_yes.setChecked(True)
                self.enrolled_no.setChecked(False)
            else:
                self.enrolled_yes.setChecked(False)
                self.enrolled_no.setChecked(True)
                self.course_select.setEnabled(False)
        # update button accordingly
        self.checkButtonState()
        
        # populate combo boxes
        self.gender.addItems(["Man", "Woman", "Other"])
        self.yr_level.addItems(["1", "2", "3", "4", "5"])
        self.updateCourseComboBox()
        self.course_select.setCurrentIndex(-1)
        
        # Functionality setup 
        
        # Connect signals to slots
        self.id_num1.textChanged.connect(self.checkButtonState)
        self.id_num2.textChanged.connect(self.checkButtonState)
        self.student_name.textChanged.connect(self.checkButtonState)
        self.enrolled_yes.toggled.connect(self.checkButtonState)
        self.enrolled_no.toggled.connect(self.checkButtonState)
        self.course_select.currentIndexChanged.connect(self.checkButtonState)
        self.yr_level.currentIndexChanged.connect(self.checkButtonState)
        self.gender.currentIndexChanged.connect(self.checkButtonState)
        self.student_create.clicked.connect(self.addButtonClicked)
        
        # Connect signals of radio buttons to handle the combo box state
        self.enrolled_yes.toggled.connect(self.handle_combo_box_state)
        self.enrolled_no.toggled.connect(self.handle_combo_box_state)
        
        # Retranslate elements in setupUI

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
        # Emit finished signals on closed
        
        MainWindow.accepted.connect(self.closed.emit)
        MainWindow.rejected.connect(self.closed.emit)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.student_create.setText(_translate("MainWindow", "Add New Student"))
        self.id_num_label.setText(_translate("MainWindow", "ID Number:"))
        self.label_2.setText(_translate("MainWindow", "-"))
        self.name_label.setText(_translate("MainWindow", "Name:"))
        self.gender_label.setText(_translate("MainWindow", "Gender:"))
        self.enrolled_label.setText(_translate("MainWindow", "Is this student enrolled?"))
        self.enrolled_yes.setText(_translate("MainWindow", "Yes"))
        self.enrolled_no.setText(_translate("MainWindow", "No"))
        self.yr_level_label.setText(_translate("MainWindow", "Year Level:"))
        self.course_select_label.setText(_translate("MainWindow", "Course:"))

    def addButtonClicked(self):
        id_num = self.id_num1.text() + "-" + self.id_num2.text()
        student_name = self.student_name.text()
        yr_level = self.yr_level.currentText()
        gender = self.gender.currentText()
        course_code = self.course_select.currentText()
        if course_code != "":
            course_code = course_code.split()[0]
        if Utils.studentValidate(id_num, student_name, yr_level, gender):
            Utils.studentCreate(id_num, student_name, yr_level, gender, course_code)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setWindowTitle("Success!")
            msg.setText("Student successfully added.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowTitle("Error!")
            msg.setText("Fill all text fields.")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            
    def updateCourseComboBox(self):
        self.course_select.clear()
        Utils.courseList(self.course_select, "courses.csv")
    
    def checkButtonState(self):
        if self.enrolled_yes.isChecked():
            if self.id_num1.text() and self.id_num2.text() and self.student_name.text() and self.course_select.currentText():
                self.student_create.setEnabled(True)
                self.student_create.setStyleSheet("background-color: #02864a; color: #fff;")
            else:
                self.student_create.setEnabled(False)
                self.student_create.setStyleSheet("background-color: gray; color: #fff;")
        elif self.enrolled_no.isChecked():
            if self.id_num1.text() and self.id_num2.text() and self.student_name.text():
                self.student_create.setEnabled(True)
                self.student_create.setStyleSheet("background-color: #02864a; color: #fff;")
            else:
                self.student_create.setEnabled(False)
                self.student_create.setStyleSheet("background-color: gray; color: #fff;")

    def handle_combo_box_state(self):
        # Enable the combo box when "Yes" is selected, disable otherwise
        if self.enrolled_yes.isChecked():
            self.course_select.setEnabled(True)
        else:
            self.course_select.setEnabled(False)

    def closeEvent(self, event):
        # Emit the 'closed' signal when the dialog is closed
        self.closed.emit()
