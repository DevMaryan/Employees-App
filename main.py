from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
import sys, os
import sqlite3
from PIL import Image

con = sqlite3.connect('employees.db')
cur = con.cursor()
defaultImg = 'images\\default.png'
employee_id = None;

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My Employees')
        self.setGeometry(450,150,750,600)
        self.UI()
        self.show()
    
    def UI(self):
        self.mainDesign()
        self.layouts()
        self.getEmployees()
        self.displayFirstRecord()

    def mainDesign(self):
        #self.setStyleSheet('font-size: 14pt; font-family: Helvetica;')
        self.employeeList = QListWidget()
        self.employeeList.itemClicked.connect(self.singleClick) # for the list on single click 
        self.btnNew = QPushButton('New')
        self.btnNew.clicked.connect(self.addEmployee)
        self.btnUpdate = QPushButton('Update')
        self.btnUpdate.clicked.connect(self.updateEmployee)
        self.btnDelete = QPushButton('Delete')
        self.btnDelete.clicked.connect(self.deleteEmployee)

    def layouts(self):
        # Main Layouts
        self.mainLayout = QHBoxLayout()

        self.leftLayout = QFormLayout()

        self.rightMainLayout = QVBoxLayout()

        self.rightTopLayout = QHBoxLayout()
        self.rightBottomLayout = QHBoxLayout()
        # Adding Child Layouts
        self.rightMainLayout.addLayout(self.rightTopLayout)
        self.rightMainLayout.addLayout(self.rightBottomLayout)
        self.mainLayout.addLayout(self.leftLayout, 60) # this 40 is like 40% view left
        self.mainLayout.addLayout(self.rightMainLayout, 40) # this 60 is like 60% view right layout
        # Adding Widgets to layout
        self.rightTopLayout.addWidget(self.employeeList)
        self.rightBottomLayout.addWidget(self.btnNew)
        self.rightBottomLayout.addWidget(self.btnUpdate)
        self.rightBottomLayout.addWidget(self.btnDelete)
        # Setting Main Window Layout
        self.setLayout(self.mainLayout)

    def addEmployee(self):
        self.newEmployee = AddEmployee() #instance of new class addEmployee
        self.close()
    
    def getEmployees(self):
        query = 'SELECT id,name,surname FROM employees'
        employees = cur.execute(query).fetchall()
        for employee in employees:
            print(employee[0], employee[1], employee[2])
            self.employeeList.addItem(str(employee[0]) + '. ' + employee[1] + ' ' + employee[2])

    def displayFirstRecord(self):
        query = "SELECT * FROM employees ORDER BY ROWID ASC LIMIT 1"
        employee = cur.execute(query).fetchone()
        print(employee)
        self.img = QLabel()
        self.img.setPixmap(QPixmap("employee_images/"+employee[5])) # employee 5 is the image, image in the db is position 5
        self.name = QLabel(employee[1])
        self.surname = QLabel(employee[2])
        self.phone = QLabel(employee[3])
        self.address = QLabel(employee[4])
        self.email = QLabel(employee[6])

        self.leftLayout.setVerticalSpacing(25) # is giving vertical padding to the labels
        self.leftLayout.setHorizontalSpacing(30) # is giving horizontal padding to the labels

        self.leftLayout.addRow('',self.img)
        self.leftLayout.addRow('Name', self.name)
        self.leftLayout.addRow('Surname', self.surname)
        self.leftLayout.addRow('Phone', self.phone)
        self.leftLayout.addRow('Email', self.email)
        self.leftLayout.addRow('Address', self.address)

    def singleClick(self):
        # The for loop is to delete the previous record and replace it with new one
        for i in reversed(range(self.leftLayout.count())):
            widget = self.leftLayout.takeAt(i).widget()

            if widget is not None:
                widget.deleteLater()
        # singleClick event continue here: 
        employee = self.employeeList.currentItem().text()
        print(employee)
        id = employee.split('.')[0]  # Get only the ID value, find the . and remove it
        print(id)
        query = ("SELECT * FROM employees WHERE id = ?")
        emp = cur.execute(query,(id,)).fetchone()
        print(emp)
        self.img = QLabel()
        self.img.setPixmap(QPixmap("employee_images/" + emp[5])) # employee 5 is the image, image in the db is position 5
        self.name = QLabel(emp[1])
        self.surname = QLabel(emp[2])
        self.phone = QLabel(emp[3])
        self.address = QLabel(emp[4])
        self.email = QLabel(emp[6])
        self.leftLayout.setVerticalSpacing(25) # is giving vertical padding to the labels
        self.leftLayout.setHorizontalSpacing(30) # is giving horizontal padding to the labels

        self.leftLayout.addRow('',self.img)
        self.leftLayout.addRow('Name', self.name)
        self.leftLayout.addRow('Surname', self.surname)
        self.leftLayout.addRow('Phone', self.phone)
        self.leftLayout.addRow('Email', self.email)
        self.leftLayout.addRow('Address', self.address)

    def deleteEmployee(self):
        if self.employeeList.selectedItems():
            employee = self.employeeList.currentitem().text()
            print(employee)
            id = employee.split('.')[0]
            mbox = QMessageBox.question(self, 'Warning', 'Are you sure you want to delete this employee', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query = "DELETE FROM employees WHERE id = ?"
                    cur.execute(query, (id,))
                    con.commit()
                    QMessageBox.information(self,'Success', 'Employee has been deleted!')
                    self.close()
                    self.main = Main()
                except:
                    QMessageBox.information(self, 'Warning', 'Employee has NOT be deleted!')
        else:
            QMessageBox.information(self, 'Warning', 'You have to select employee first!')

    def updateEmployee(self):
        global employee_id
        if self.employeeList.selectedItems():
            employee = self.employeeList.currentItem().text()
            employee_id = employee.split('.')[0]
            print(employee_id)
            self.updateWindow = UpdateEmployee()
            self.close()
        else:
            QMessageBox.information(self, 'Warning', 'Please select employee first')


class UpdateEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Employee')
        self.setGeometry(450,150,350,600)
        self.UI()
        self.show()


    def UI(self):
        self.getEmployee()
        self.mainDesign()
        self.layouts()

    def closeEvent(self, event):
        self.main = Main()

    def getEmployee(self):
        global employee_id
        # print('employee id', employee_id)
        query = 'SELECT * FROM employees WHERE id = ?'
        employee = cur.execute(query,(employee_id,)).fetchone()
        print(employee)
        self.name = employee[1]
        self.surname = employee[2]
        self.phone = employee[3]
        self.email = employee[4]
        self.image = employee[5]
        self.address = employee[6]


    def mainDesign(self): 
        # Top Layout Widgets
        # self.setStyleSheet('background-color:#e0e0e0; font-size:14pt; font-family:Helvetica;') # form background color
        self.title_lbl = QLabel('Update Employee')
        #self.title_lbl.setStyleSheet('font-size:20pt;font-family:Helvetica;background-color:#e0e0e0;')
        self.imgAdd_lbl = QLabel()
        self.imgAdd_lbl.setPixmap(QPixmap('employee_images\\{}'.format(self.image)))

        # Bottom layout Widgets
        self.name_lbl = QLabel('Name')
        self.name_entry = QLineEdit()
        self.name_entry.setText(self.name)
        self.surname_lbl = QLabel('Surname')
        self.surname_entry = QLineEdit()
        self.surname_entry.setText(self.surname)
        self.phone_lbl = QLabel('Phone')
        self.phone_entry = QLineEdit()
        self.phone_entry.setText(self.phone)
        self.email_lbl = QLabel('Email')
        self.email_entry = QLineEdit()
        self.email_entry.setText(self.email)
        self.picture_lbl = QLabel('Picture')
        self.picture_btn = QPushButton('Browse')
        self.picture_btn.clicked.connect(self.uploadImage)
        #self.picture_btn.setStyleSheet('background-color:#e0e0e0; font-size:10pt;')
        self.address_lbl = QLabel('Address')
        self.address_Editor = QTextEdit()
        self.address_Editor.setText(self.address)
        self.update_btn = QPushButton('Update')
        self.update_btn.clicked.connect(self.updateEmployee)


    def layouts(self):
        # Main layouts
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()

        # Child Layouts
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        # Adding widgets to layouts
            # Top Layout #
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title_lbl)
        self.topLayout.addWidget(self.imgAdd_lbl)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(110,20,10,30) #left, top, right, bottom
            # Bottom Layout #
        self.bottomLayout.addRow(self.name_lbl, self.name_entry)
        self.bottomLayout.addRow(self.surname_lbl, self.surname_entry)
        self.bottomLayout.addRow(self.phone_lbl, self.phone_entry)
        self.bottomLayout.addRow(self.email_lbl, self.email_entry)
        self.bottomLayout.addRow(self.picture_lbl, self.picture_btn)
        self.bottomLayout.addRow(self.address_lbl, self.address_Editor)
        self.bottomLayout.addRow('', self.update_btn) # '' is taking space for widget

        # Setting Main Layout for Window
        self.setLayout(self.mainLayout)

    def uploadImage(self):
        global defaultImg
        size = (130,130)
        try:
            self.fileName, ok = QFileDialog.getOpenFileName(self, 'Upload Image', '', 'Image Files (*.jpg *.png)')
            defaultImg = os.path.basename(self.fileName)
            print(defaultImg)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save('employee_images\\{}'.format(defaultImg))
        except EOFError as e:
            print(e)

    def updateEmployee(self):
        global defaultImg
        global employee_id
        name = self.name_entry.text()
        surname = self.surname_entry.text()
        phone = self.phone_entry.text()
        email = self.email_entry.text()
        img = defaultImg
        address = self.address_Editor.toPlainText()
        
        if(name and surname and phone and email != ''):
            try:
                query = "UPDATE employees SET name = ?, surname = ?, phone = ?, email = ?, image = ?, address = ? WHERE id = ?"
                cur.execute(query,(name, surname, phone, email, img, address, employee_id))
                con.commit()
                QMessageBox.information(self, 'Success', 'Employee has beed successfully updated!')
                self.close() # second way and below
                self.main = Main() #Second way to close the window and return to the main window
            except EOFError as e:
                QMessageBox.information(self, 'Error', 'Employee has NOT beed updated!')
                print(e)
        else:
            QMessageBox.information(self, 'Warning', 'Name, Surname, Phone and Email fields can NOT be empty!')


class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Add Employees')
        self.setGeometry(450,150,350,600)
        self.UI()
        self.show()

    def closeEvent(self, event): # on close window app, new instance of Main class(window) will be open
        self.main = Main() 

    def UI(self):
        self.mainDesign()
        self.layouts()

    def mainDesign(self): 
        # Top Layout Widgets
        # self.setStyleSheet('background-color:#e0e0e0; font-size:14pt; font-family:Helvetica;') # form background color
        self.title_lbl = QLabel('Add Employee')
        #self.title_lbl.setStyleSheet('font-size:20pt;font-family:Helvetica;background-color:#e0e0e0;')
        self.imgAdd_lbl = QLabel()
        self.imgAdd_lbl.setPixmap(QPixmap('images\\default.png'))

        # Bottom layout Widgets
        self.name_lbl = QLabel('Name')
        self.name_entry = QLineEdit()
        self.name_entry.setPlaceholderText('Enter employee name')
        self.surname_lbl = QLabel('Surname')
        self.surname_entry = QLineEdit()
        self.surname_entry.setPlaceholderText('Enter employee surname')
        self.phone_lbl = QLabel('Phone')
        self.phone_entry = QLineEdit()
        self.phone_entry.setPlaceholderText('Enter employee phone number')
        self.email_lbl = QLabel('Email')
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText('Enter employee email')
        self.picture_lbl = QLabel('Picture')
        self.picture_btn = QPushButton('Browse')
        #self.picture_btn.setStyleSheet('background-color:#e0e0e0; font-size:10pt;')
        self.picture_btn.clicked.connect(self.uploadImage)
        self.address_lbl = QLabel('Address')
        self.address_Editor = QTextEdit()
        self.add_btn = QPushButton('Add')
        self.add_btn.clicked.connect(self.addEmployee)

    def layouts(self):
        # Main layouts
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()

        # Child Layouts
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        # Adding widgets to layouts
            # Top Layout #
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.title_lbl)
        self.topLayout.addWidget(self.imgAdd_lbl)
        self.topLayout.addStretch()
        self.topLayout.setContentsMargins(110,20,10,30) #left, top, right, bottom
            # Bottom Layout #
        self.bottomLayout.addRow(self.name_lbl, self.name_entry)
        self.bottomLayout.addRow(self.surname_lbl, self.surname_entry)
        self.bottomLayout.addRow(self.phone_lbl, self.phone_entry)
        self.bottomLayout.addRow(self.email_lbl, self.email_entry)
        self.bottomLayout.addRow(self.picture_lbl, self.picture_btn)
        self.bottomLayout.addRow(self.address_lbl, self.address_Editor)
        self.bottomLayout.addRow('', self.add_btn) # '' is taking space for widget

        # Setting Main Layout for Window
        self.setLayout(self.mainLayout)

    def uploadImage(self):
        global defaultImg
        size = (130,130)
        try:
            self.fileName, ok = QFileDialog.getOpenFileName(self, 'Upload Image', '', 'Image Files (*.jpg *.png)')
            defaultImg = os.path.basename(self.fileName)
            print(defaultImg)
            img = Image.open(self.fileName)
            img = img.resize(size)
            img.save('employee_images\\{}'.format(defaultImg))
        except EOFError as e:
            print(e)

    def addEmployee(self):
        global defaultImg
        name = self.name_entry.text()
        surname = self.surname_entry.text()
        phone = self.phone_entry.text()
        email = self.email_entry.text()
        img = defaultImg
        address = self.address_Editor.toPlainText()
        
        if(name and surname and phone and email != ''):
            try:
                query = "INSERT INTO employees (name, surname, phone, email, image, address) VALUES (?, ?, ?, ?, ?, ?)"
                cur.execute(query,(name, surname, phone, email, img, address))
                con.commit()
                QMessageBox.information(self, 'Success', 'Employee has beed successfully added!')
                self.close() # second way and below
                self.main = Main() #Second way to close the window and return to the main window
            except EOFError as e:
                QMessageBox.information(self, 'Error', 'Employee has NOT beed added!')
                print(e)
        else:
            QMessageBox.information(self, 'Warning', 'Name, Surname, Phone and Email fields can NOT be empty!')



def main():
    APP = QApplication(sys.argv)
    window = Main() #Instance of the class Main
    sys.exit(APP.exec_())


if __name__ == '__main__':
    main()
    