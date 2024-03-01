from PyQt5 import QtCore, QtWidgets
from utils import Utils


class CoursePopup(QtWidgets.QDialog):
    
    # Define signals
    closed = QtCore.pyqtSignal()
    courseAdded = QtCore.pyqtSignal()
    
    def setupUi(self, MainWindow, mode, course_code=None, course_description=None):
        
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
        self.addCourseBtn.setEnabled(False)  # Initially disabled
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Set Initial States
        
        # Adjust fields based on the mode
        self.addCourseBtn.clicked.connect(self.closeEvent)
        if mode == 'create':
            self.addCourseBtn.setText("Add Course")
            self.addCourseBtn.setStyleSheet("background-color: #02864A; color: #fff;")
            self.course_code.setReadOnly(False)
            self.course_description.setReadOnly(False)
            self.course_code.setFocus()
            self.course_code.clear()
            self.course_description.clear()
            self.course_code.setStyleSheet("background-color: #FFFFFF;")
            self.course_description.setStyleSheet("background-color: #FFFFFF;")
            self.addCourseBtn.clicked.connect(self.addCourse)
        elif mode == 'edit':
            self.addCourseBtn.setText("Edit Course")
            self.addCourseBtn.setStyleSheet("background-color: #FB8D1A; color: #fff;")
            self.course_code.setReadOnly(True)
            self.course_description.setReadOnly(False)
            self.course_code.setStyleSheet("background-color: #F0F0F0;")
            self.course_description.setStyleSheet("background-color: #FFFFFF;")
            self.course_code.setText(course_code)
            self.course_description.setText(course_description)
            self.course_description.setFocus()
            self.addCourseBtn.clicked.connect(self.editCourse)
            self.addCourseBtn.setEnabled(True)  # Enable the button for editing
        elif mode == 'delete':
            self.addCourseBtn.setText("Delete Course")
            self.addCourseBtn.setStyleSheet("background-color: #E8083E; color: #fff;")
            self.course_code.setReadOnly(True)
            self.course_description.setReadOnly(True)
            self.course_code.setStyleSheet("background-color: #F0F0F0;")
            self.course_description.setStyleSheet("background-color: #F0F0F0;")
            self.course_code.setText(course_code)
            self.course_description.setText(course_description)
            self.addCourseBtn.clicked.connect(self.deleteCourse)
            self.addCourseBtn.setEnabled(True)  # Enable the button for deleting

    # Method definitions for setupUI functionality
    
    def addCourse(self):
        course_code = self.course_code.text()
        course_description = self.course_description.text()
        if course_code and course_description:
            Utils.courseCreate(course_code, course_description)
            self.courseAdded.emit()
            self.showSuccessMessage("Course added successfully!")
        else:
            self.showErrorMessage("Fill all text fields.")

    def editCourse(self):
        course_code = self.course_code.text()
        new_course_description = self.course_description.text()
        if course_code and new_course_description:
            Utils.courseUpdate(course_code, new_course_description)
            self.courseAdded.emit()
            self.close()
            self.showSuccessMessage("Course edited successfully!")
        else:
            self.showErrorMessage("Fill all text fields.")

    def deleteCourse(self):
        course_code = self.course_code.text()
        if Utils.courseDelete(course_code):
            self.courseAdded.emit()
            self.close()
            self.showSuccessMessage("Course deleted successfully!")
        else:
            self.showErrorMessage("An error occurred while deleting the course.")

    def showSuccessMessage(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def showErrorMessage(self, message):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText(message)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        
    def closeEvent(self, event):
        # Get the selected course from the Ui_mainWindow instance
        selected_course = self.parent().selected_course
        if selected_course:
            self.courseSelectComboBox.setCurrentText(selected_course)

    # Retranslate elements in setupUI
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.course_code_label.setText(_translate("MainWindow", "Course Code:"))
        self.course_description_label.setText(_translate("MainWindow", "Course Description:"))
        self.addCourseBtn.setText(_translate("MainWindow", "Add Course"))
