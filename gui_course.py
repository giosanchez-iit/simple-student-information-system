from PyQt5 import QtCore, QtWidgets
from utils import Utils


class CoursePopup(QtWidgets.QDialog):
    
    # Define signals
    closed = QtCore.pyqtSignal()
    courseAdded = QtCore.pyqtSignal()
    
    def setupUi(self, MainWindow):
        
        # Graphics Interface Setup
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 140)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.course_code_label = QtWidgets.QLabel(self.centralwidget)
        self.course_code_label.setGeometry(QtCore.QRect(20, 20, 71, 20))
        self.course_code_label.setObjectName("course_code_label")
        self.course_description_label = QtWidgets.QLabel(self.centralwidget)
        self.course_description_label.setGeometry(QtCore.QRect(20, 50, 101, 20))
        self.course_description_label.setObjectName("course_description_label")
        self.course_code = QtWidgets.QLineEdit(self.centralwidget)
        self.course_code.setGeometry(QtCore.QRect(140, 20, 311, 20))
        self.course_code.setObjectName("course_code")
        self.course_description = QtWidgets.QLineEdit(self.centralwidget)
        self.course_description.setGeometry(QtCore.QRect(140, 50, 311, 20))
        self.course_description.setObjectName("course_description")
        self.addCourseBtn = QtWidgets.QPushButton(self.centralwidget)
        self.addCourseBtn.setGeometry(QtCore.QRect(190, 90, 101, 23))
        self.addCourseBtn.setStyleSheet("background-color: gray; color: #fff;")
        self.addCourseBtn.setObjectName("addCourseBtn")
        self.addCourseBtn.setEnabled(True)  # Initially disabled
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        # Functionality setup 
        
        # connect signals to check if both fields are filled
        self.course_code.textChanged.connect(self.check_fields_filled)
        self.course_description.textChanged.connect(self.check_fields_filled)

        # connect button clicked signal to the add_course method
        self.addCourseBtn.clicked.connect(self.add_course)
        
    # Method definitions for setupUI functionality
    
    def check_fields_filled(self):
        # Enable the button only when both text fields are filled
        if self.course_code.text() and self.course_description.text():
            self.addCourseBtn.setEnabled(True)
            self.addCourseBtn.setStyleSheet("background-color: #02864a; color: #fff;")
        else:
            self.addCourseBtn.setEnabled(False)
            self.addCourseBtn.setStyleSheet("background-color: gray; color: #fff;")

    def add_course(self):
        # add the details from the text fields into the CSV
        course_code = self.course_code.text()
        course_description = self.course_description.text()
        Utils.courseCreate(course_code, course_description)

        # emit signal to update combo box in main window
        self.courseAdded.emit()
        
        # create a message box to show successful operation
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(f"{course_code} - {course_description} added successfully!")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
    

    # Retranslate elements in setupUI
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.course_code_label.setText(_translate("MainWindow", "Course Code:"))
        self.course_description_label.setText(_translate("MainWindow", "Course Description:"))
        self.addCourseBtn.setText(_translate("MainWindow", "Add Course"))
