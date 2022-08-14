from PySide6 import QtCore, QtGui, QtWidgets
import sys
import main
from datetime import datetime, date
import os.path
import pickle
import my_calendar
import schedule_gui

class period:
    
    def __init__(self, time, label=None):
        self.time = time
        self.label = label
        self.minutes = int(self.time % 1 * 60)
        self.hours = int(self.time - (self.time % 1))
        
    def google_time(self):
        time = datetime(date.today().year, date.today().month, date.today().day, self.hours, self.minutes)
        return time
    
    def actual_time(self):
        minutes = self.minutes
        hours = self.hours
        if minutes == 0:
            minutes = "00"
        if hours > 12:
            hours -= 12
        return f"{hours}:{minutes}"

def isformatted(unformatted_time):
    try:
        time = unformatted_time.split()[0]
        ampm = unformatted_time.split()[1].upper()
    except:
        return False
    if ampm != "AM" and ampm != "PM":
        return False
    try:
        first_time = time.split(":")[0]
        second_time = time.split(":")[1]
    except:
        return False
    try:
        int(first_time)
        int(second_time)
    except:
        return False
    return True

def isformatted2(duration):
    try:
        first_time = duration.split(":")[0]
        second_time = duration.split(":")[1]
    except:
        return False
    try:
        int(first_time)
        int(second_time)
    except:
        return False
    return True

def formatter(unformatted_time):
    time = unformatted_time.split()[0]
    ampm = unformatted_time.split()[1].upper()
    hours = int(time.split(":")[0])
    minutes = int(time.split(":")[1]) / 60
    if ampm == "PM" and hours >= 1:
        hours += 12
    return hours + minutes

def formatter2(duration):
    hours = int(duration.split(":")[0])
    minutes = int(duration.split(":")[1]) / 60
    return hours + minutes

class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.resize(640, 320)
        MainWindow.setStyleSheet("background-color: AliceBlue;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.time_list = []
 
        self.pushButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton5 = QtWidgets.QPushButton(self.centralwidget)

        self.pushButton1.setGeometry(QtCore.QRect(60,  270, 93, 28))
        self.pushButton2.setGeometry(QtCore.QRect(160, 270, 93, 28))
        self.pushButton3.setGeometry(QtCore.QRect(260, 270, 93, 28))
        self.pushButton4.setGeometry(QtCore.QRect(360, 270, 93, 28))
        self.pushButton5.setGeometry(QtCore.QRect(460, 270, 93, 28))

        if os.path.exists("time_list.obj"):
            self.pushButton1.hide()  
            self.pushButton2.hide()
            self.pushButton3.setGeometry(QtCore.QRect(160, 270, 93, 28))
            self.pushButton4.setGeometry(QtCore.QRect(260, 270, 93, 28))
            self.pushButton5.setGeometry(QtCore.QRect(360, 270, 93, 28))  
            file = open("time_list.obj", 'rb')
            self.time_list = pickle.load(file)
            file.close()
 
        # For displaying confirmation message along with user's info.
        self.label = QtWidgets.QLabel(self.centralwidget)   
        self.label.setGeometry(QtCore.QRect(250, 30, 450, 250))
 
        # Keeping the text of label empty initially.      
        self.label.setText("Hi, Welcome to No Brainer")    
 
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("No Brainer", "No Brainer"))
        self.pushButton1.setText(_translate("No Brainer", "Wake/Sleep"))
        self.pushButton2.setText(_translate("No Brainer", "My Routine"))
        self.pushButton3.setText(_translate("No Brainer", "Tasks for Today"))
        self.pushButton4.setText(_translate("No Brainer", "Show Schedule"))
        self.pushButton5.setText(_translate("No Brainer", "Update Google"))

        self.pushButton1.clicked.connect(self.create_time_list)
        self.pushButton2.clicked.connect(self.get_fixed_tasks)
        self.pushButton3.clicked.connect(self.get_daily_tasks)
        self.pushButton4.clicked.connect(self.display_schedule)
        self.pushButton5.clicked.connect(self.create_gc_events)

    def create_gc_events(self):
        schedule = []
        previous_label = ""
        start_time = None
        end_time = None
        start_counting = False
        for time in self.time_list:
            label = time.label
            if label != previous_label and start_counting:
                end_time = time.google_time()
                schedule.append((previous_label, start_time, end_time,))
                start_counting = False
            if label != previous_label and not start_counting:
                start_time = time.google_time()
                start_counting = True
            if label == previous_label and start_counting:
                pass
            previous_label = label

        service = my_calendar.initialize_calendar()
        for name, start, end, in schedule:
            color = 4
            if name == None:
                name = "Work/Free Time"

            my_calendar.create_event(start, end, name, service)

        self.label.setText("No Brainer Has Updated Your Google Calendar!\n Enjoy your productive day!")
        
    def display_schedule(self):
        schedule = []
        previous_label = ""
        start_time = None
        end_time = None
        start_counting = False
        for time in self.time_list:
            label = time.label
            if label != previous_label and start_counting:
                end_time = time.actual_time()
                schedule.append((previous_label, start_time, end_time))
                start_counting = False
            if label != previous_label and not start_counting:
                start_time = time.actual_time()
                start_counting = True
            if label == previous_label and start_counting:
                pass
            previous_label = label

        combined = ''
        for name, start, end in schedule:
            combined += f"{name} : {start} - {end}\n"
        self.label.setText(combined)
        #testStr = "1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n"
        #self.label.setText(testStr)
   
    def create_time_list(self):
        while True:
            start_time, done1 = QtWidgets.QInputDialog.getText(
                     self, 'Input Dialog', 'What time do you start your day? :')
            if isformatted(start_time):
                start_time = formatter(start_time)
                break

        while True:
            end_time, done1 = QtWidgets.QInputDialog.getText(
                     self, 'Input Dialog', 'What time do you end your day? :')
            if isformatted(end_time):
                end_time = formatter(end_time)
                break
        
        alive_time = int(end_time - start_time)
        new_time = start_time
        for i in range(0, alive_time*4 +1):
            self.time_list.append(period(new_time))
            new_time += 0.25

    def display_time_list(self):
        for time in self.time_list:
            print(f"{time.label} - {time.actual_time()}")

    def append_tasks(self, fixed_tasks):
        for name, start_time, end_time, in fixed_tasks:
            name_activated = False
            for index, period in enumerate(self.time_list):
                if period.time == start_time:
                    name_activated = True
                if name_activated:
                    period.label = name
                if index == len(self.time_list)-1:
                    name_activated = False
                elif self.time_list[index+1].time == (end_time):
                    name_activated = False

    def append_daily_tasks(self, daily_tasks):
        daily_tasks.sort(key=lambda x: x[1], reverse=True)
        for name, task_duration, in daily_tasks:
            empty_slots = self.get_empty_times()
            empty_slots.sort(key=lambda x: x[1])
            for start, slot_duration in empty_slots:
                    if task_duration <= slot_duration:
                        self.append_tasks([(name, start, start+(task_duration))])
                        break

    def get_empty_times(self):
        period_sizes = []
        name_activated = False
        start_time = None
        end_time = None
        for index, time in enumerate(self.time_list):
                if name_activated and time.label != None:
                    end_time = time.time - 0.25
                    duration = end_time - start_time
                    period_sizes.append((start_time, duration))
                    name_activated = False
                elif name_activated and index == len(self.time_list)-1:
                    end_time = time.time
                    duration = end_time - start_time
                    period_sizes.append((start_time, duration))
                    name_activated = False
                if name_activated:
                    continue
                if time.label == None:
                    name_activated = True
                    start_time = time.time
        return period_sizes

    def get_fixed_tasks(self):
        fixed_tasks = []

        while True:
            name, done1 = QtWidgets.QInputDialog.getText(
                 self, 'Input Dialog', 'What is the name of the fixed task? :')

            while True:

                start_time, done2 = QtWidgets.QInputDialog.getText(
                   self, 'Input Dialog', 'Enter your start time :') 

                if isformatted(start_time):
                    break

            while True:

                end_time, done2 = QtWidgets.QInputDialog.getText(
                   self, 'Input Dialog', 'Enter your end time :') 

                if isformatted(end_time):
                    break

                self.label.setText("Duration needs to be entered in this format: hrs:min ")

            fixed_tasks.append((name, formatter(start_time), formatter(end_time)))
            user = ""  
            while (user.upper() != "Y" and user.upper() != "N"):
                user, done3 = QtWidgets.QInputDialog.getText(
                   self, 'Input Dialog', "Do you want to input another fixed task? (Y/N) ") 
            if user.upper() == "N":
                print(fixed_tasks)
                self.append_tasks(fixed_tasks)
                break

        file = open("time_list.obj", 'wb')
        pickle.dump(self.time_list, file)
         
    def get_daily_tasks(self):
        daily_tasks = []

        while True:
            name, done1 = QtWidgets.QInputDialog.getText(
                 self, 'Input Dialog', 'What is the name of the daily task? :')
            while True:

                duration, done2 = QtWidgets.QInputDialog.getText(
                   self, 'Input Dialog', 'How long will this task take? :') 

                if isformatted2(duration):
                    break

                self.label.setText("Duration needs to be entered in this format: hrs:min ")
            daily_tasks.append((name, formatter2(duration)))
            user = ""  
            while (user.upper() != "Y" and user.upper() != "N"):
                user, done3 = QtWidgets.QInputDialog.getText(
                   self, 'Input Dialog', "Do you want to input another daily task? (Y/N) ") 
            if user.upper() == "N":
                print(daily_tasks)
                self.append_daily_tasks(daily_tasks)
                self.display_time_list()
                break   
               
              
              
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show() 
    sys.exit(app.exec_())