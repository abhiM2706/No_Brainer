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

def create_time_list():
    time_list = []
    while True:
        start_time = input("What time do you start your day: ")
        if isformatted(start_time):
            start_time = formatter(start_time)
            break
        print("Time needs to be entered in this format: --:-- AM/PM")
    while True:
        end_time = input("What time do you end your day: ")
        if isformatted(end_time):
            end_time = formatter(end_time)
            break
        print("Time needs to be entered in this format: --:-- AM/PM")
    alive_time = int(end_time - start_time)
    new_time = start_time
    for i in range(0, alive_time*4 +1):
        time_list.append(period(new_time))
        new_time += 0.25
        
    return time_list

def get_empty_times(time_list):
    period_sizes = []
    name_activated = False
    start_time = None
    end_time = None
    for index, time in enumerate(time_list):
            if name_activated and time.label != None:
                end_time = time.time - 0.25
                duration = end_time - start_time
                period_sizes.append((start_time, duration))
                name_activated = False
            elif name_activated and index == len(time_list)-1:
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

def get_fixed_tasks():
    fixed_tasks = []
    while True:
        name = input("What is the name of the fixed task?")
        while True:
            start_time = input("Enter your start time: ")
            if isformatted(start_time):
                break
            print("Time needs to be entered in this format: --:-- AM/PM")
        while True:
            end_time = input("Enter your end time: ")
            if isformatted(end_time):
                break
            print("Time needs to be entered in this format: --:-- AM/PM")
        fixed_tasks.append((name, formatter(start_time), formatter(end_time)))
        user = ""  
        while (user.upper() != "Y" and user.upper() != "N"):
            user = input("Do you want to input another fixed task? (Y/N) ")
        if user.upper() == "N":
            return fixed_tasks 

def append_tasks(fixed_tasks, time_list):
    for name, start_time, end_time in fixed_tasks:
        name_activated = False
        for index, period in enumerate(time_list):
            if period.time == start_time:
                name_activated = True
            if name_activated:
                period.label = name
            if index == len(time_list)-1:
                name_activated = False
            elif time_list[index+1].time == (end_time):
                name_activated = False

def get_daily_tasks():
    daily_tasks = []
    while True:
        name = input("What is the name of the daily task? ")
        while True:
            duration = input("How long will this task take: ")
            if isformatted2(duration):
                break
            print("Duration needs to be entered in this format: hrs:min ")
        daily_tasks.append((name, formatter2(duration)))
        user = ""  
        while (user.upper() != "Y" and user.upper() != "N"):
            user = input("Do you want to input another fixed task? (Y/N) ")
        if user.upper() == "N":
            return daily_tasks 

def append_daily_tasks(daily_tasks, time_list):
    daily_tasks.sort(key=lambda x: x[1], reverse=True)
    for name, task_duration in daily_tasks:
        empty_slots = get_empty_times(time_list)
        empty_slots.sort(key=lambda x: x[1])
        for start, slot_duration in empty_slots:
                if task_duration <= slot_duration:
                    append_tasks([(name, start, start+(task_duration))], time_list)
                    break

def display_schedule(time_list):
    schedule = []
    previous_label = ""
    start_time = None
    end_time = None
    start_counting = False
    for time in time_list:
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
    for name, start, end in schedule:
        print(f"{name} : {start} - {end}")

def make_gc_schedule(time_list):
    schedule = []
    previous_label = ""
    start_time = None
    end_time = None
    start_counting = False
    for time in time_list:
        label = time.label
        if label != previous_label and start_counting:
            end_time = time.google_time()
            schedule.append((previous_label, start_time, end_time))
            start_counting = False
        if label != previous_label and not start_counting:
            start_time = time.google_time()
            start_counting = True
        if label == previous_label and start_counting:
            pass
        previous_label = label
    return schedule

def create_gc_events(schedule, service):
	for name, start, end in schedule:
		if name == None:
			name = "Work/Free Time"
		
		my_calendar.create_event(start, end, name, service)

if __name__ == "__main__":

    time_list = []

    if os.path.exists("time_list.obj"):
    	file = open("time_list.obj", 'rb')
    	time_list = pickle.load(file)
    	file.close()

    else:
    	time_list = create_time_list()
    	fixed_tasks = get_fixed_tasks()
    	append_tasks(fixed_tasks=fixed_tasks, time_list=time_list)
    	file = open("time_list.obj", 'wb')
    	pickle.dump(time_list, file)

    daily_tasks = get_daily_tasks()
    append_daily_tasks(daily_tasks, time_list)
    display_schedule(time_list)
    schedule = make_gc_schedule(time_list)
    service = my_calendar.initialize_calendar()
    create_gc_events(schedule, service)






