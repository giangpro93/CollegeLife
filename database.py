import datetime
import json
from werkzeug.utils import secure_filename

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("./college-life-7a8dc-firebase-adminsdk-3tl96-e412912881.json")
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://college-life-7a8dc.firebaseio.com',
    'storageBucket': 'college-life-7a8dc.appspot.com/'
})
root = db.reference()
users_ref = root.child('users')
groups_ref = root.child('groups')
events_ref = root.child('events')


def CheckCredentials(username,password):
    users = users_ref.get()
    if (users == None):
        return False
    for key, val in users.items():
        if username == key and password == val['password']:
            return "user"

    groups = groups_ref.get()
    if (groups == None):
        return False
    for key, val in groups.items():
        if username == key and password == val['password']:
            return "group"

    return "False"


def UserExists(username):
    users = users_ref.get()
    if (users == None):
        return False
    for key, val in users.items():
        if username == key:
            return True
    return False


def GroupExists(username):
    groups = groups_ref.get()
    if (groups == None):
        return False
    for key, val in groups.items():
        if username == key:
            return True
    return False


def AddUser(username, password):
    if UserExists(username):
        return False

    users_ref.child(username).set({
        'password': password
    })
    return True


def AddGroup(username, password):
    if GroupExists(username):
        return False

    groups_ref.child(username).set({
        'password': password
    })
    return True


def AddNewEvent(groupID, title, timeFrom, timeTo, date, address):
    root.child('events').child(title).set({
        'timeFrom': timeFrom,
        'timeTo': timeTo,
        'date': date,
        'address': address
    })
    groups_ref.child(groupID).child('listEvents').update({
        title: True
    })
    return True


def subscribeGroup(username, groupID):
    users_ref.child(username).child('listGroups').update({
        groupID: True
    })
    return True

def updateFreetime(username, freetime):
    users_ref.child(username).update({
        'freetime': freetime
    })
    return True

def addTaskToDB(username, taskName, taskDuration):
    users_ref.child(username).child('listTasks').update({
        taskName: taskDuration
    })
    return True

def fetchEventsFromDB(username):
    res = []
    print(username)
    ListGroups = users_ref.child(username).child('listGroups').get()
    ListEvents = users_ref.child(username).child('listEvents').get()
    for group, val in ListGroups.items():
        ListGroupsEvents = groups_ref.child(group).child('listEvents').get()
        for eventName, dumbVar in ListGroupsEvents.items():
            eventObj = events_ref.child(eventName).get()
            info = eventName + "<br> Time: " + eventObj['timeFrom'] + " - " + eventObj['timeTo'] + "<br> Date: " + eventObj['date'] + "<br> Address: " + eventObj['address']
            going = ListEvents != None and (eventName in ListEvents) and ListEvents[eventName]
            res.append({
                "info": info,
                "groupID": group,
                "going": going,
                "eventID": eventName
            }
    )
    return json.dumps(res)

def isConflict(event1, event2):
    if (events_ref.child(event1).get()['date'] == events_ref.child(event2).get()['date']):
        return True
    else:
        return False

def updateGoingStatusToDB(username, eventID, going):
    if going:
        for key, val in users_ref.child(username).child('listEvents').get().items():
            if val and isConflict(eventID, key):
                return "Failed"

    users_ref.child(username).child('listEvents').update({
        eventID: going
    })

    return "Succeed"