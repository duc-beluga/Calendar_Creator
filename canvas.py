from asyncio import events
from ctypes import sizeof
from canvasapi import Canvas
from datetime import datetime
from openpyxl import Workbook
import numpy as np
import pandas as pd

api_url = 'https://gatech.instructure.com/'
api_key = '2096~9ILml1dfbsTmXHNxSfjHo4Vupc9L9Q8d2ueI3G972Lmk5qeYXo44lCGBDVbGhjTX'
canvas = Canvas(api_url, api_key)
courses = canvas.get_courses(state="available", enrollment_state="active")
user = canvas.get_current_user()

# for course in courses:
#     course = str(course)
#     events = canvas.get_calendar_events(context_codes=[f"course_{course[-7:-1]}"], end_date="2022-05-07T23:59:59Z")
#     for event in events:
#         print(event)

wb = Workbook()
ws = wb.active
ws.title = "Schedule"
ws.append(["Course Name", "Assignment name", "Due Date"])
data = []
count = 0
for course in courses:
    assignments = user.get_assignments(course)
    for assignment in assignments:
        if (type(assignment.due_at) == str): 
            due_date = datetime.strptime(assignment.due_at, "%Y-%m-%dT%H:%M:%SZ")
        else:
            due_date = "No due date"
        data.append([course.course_code, assignment.name, due_date])
        print(type(data[0][2]))
        data = sorted(data, key=lambda x:x[2])
        print(assignment.name, "Due at: ", due_date)
    count = count + 1
    if (count == 2):
        break

for row in data:
    ws.append(row)
wb.save('Schedule.xlsx')





