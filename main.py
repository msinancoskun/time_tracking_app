import time
import psutil
import json
from datetime import datetime
from pywinauto import Desktop
import wmi
from win32gui import GetForegroundWindow
import win32process


def create_jsonfile():
    with open('all_activities.json', 'w') as json_file:
        json.dump(activities, json_file, indent=4, sort_keys=True)

    # with open('current_working_apps.json', 'w') as json_file:
    #     json.dump(current_working_apps, json_file)


wmi_constructor = wmi.WMI()

active_app = ""
activities = []
current_working = []

current_user = "Current User: " + psutil.users()[0].name
now = datetime.now()
current_time = now.strftime("%m/%d/%Y, %H:%M:%S")

windows = Desktop(backend="uia").windows()
# current_working_apps = [w.window_text() for w in windows]





for processes in psutil.process_iter(["pid", "name", "username", "status"]):
    app_name = processes.info["name"]
    status = processes.info["status"]
    pid = processes.info["pid"]
    start_time = datetime.fromtimestamp(processes.create_time())
    current_app = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1]).name()
    active_app = current_app
    current_working.append(active_app)

    if app_name not in activities and current_app == app_name:
        activities.append({"activities": {app_name[0]: [pid,
                                                        status,
                                                        str(current_time),
                                                        str(start_time),
                                                        ]
                                        }
                        })
        active_app = app_name
print(active_app)
        

create_jsonfile()
