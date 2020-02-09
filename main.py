from flask import Flask, render_template, request, Response, redirect, session, url_for, g, send_file, jsonify, flash
from glob import glob
import os.path
import json
import hashlib
from werkzeug.utils import secure_filename

from database import CheckCredentials, AddUser, AddGroup, AddNewEvent, subscribeGroup, updateFreetime, addTaskToDB, fetchEventsFromDB, updateGoingStatusToDB

app = Flask(__name__)
app.secret_key = os.urandom(24)
isUser = True


@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/', methods=['GET'])
def main():
    if not g.user:
        return render_template('index.html')
    if (isUser):
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('group'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    global isUser

    if g.user:
        return main()

    if request.method == 'POST':
        s = request.form.to_dict()['login_info']
        json_acceptable_string = s.replace("'", "\"")
        d = json.loads(json_acceptable_string)

        h = hashlib.md5(d['password'].encode())
        hashed_password = h.hexdigest()

        checkResult = CheckCredentials(d['username'], hashed_password);

        if (checkResult == "False"):
            return ("False")

        session['user'] = d['username']

        if (checkResult == 'user'):
            isUser = True
            return ("True")

        if (checkResult == 'group'):
            isUser = False
            return ("True")

    print(isUser)

    ##returns template if its not a POST
    return render_template('index.html')


@app.route('/createUser', methods=['GET', 'POST'])
def createUser():

    s = request.form.to_dict()['json_string']
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)

    h = hashlib.md5(d['password'].encode())
    hashed_password = h.hexdigest()

    if AddUser(d['username'], hashed_password):
        ##starts session with this user
        session['user'] = d['username']
    else:
        return "False"

    return render_template('index.html')


@app.route('/createGroup', methods=['GET', 'POST'])
def createGroup():

    s = request.form.to_dict()['json_string']
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)

    h = hashlib.md5(d['password'].encode())
    hashed_password = h.hexdigest()

    if AddGroup(d['username'], hashed_password):
        ##starts session with this user
        session['user'] = d['username']
    else:
        return "False"

    return render_template('index.html')


@app.route('/createNewEvent', methods=['GET', 'POST'])
def createNewEvent():

    s = request.form.to_dict()['json_string']
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)

    if AddNewEvent(g.user, d['title'], d['timeFrom'], d['timeTo'], d['date'], d['address']):
        return "True"
    else:
        return "False"


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if g.user and isUser:
        return render_template('profile.html', user=g.user)
    return main()


@app.route('/group', methods=['GET', 'POST'])
def group():
    if g.user and not isUser:
        return render_template('addEvent.html', user=g.user)
    return main()


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# @app.route('/user/images')
# def getCurrentUserImages():
#     """Gets all images that belong to current user
#
#     Returns:
#         str: JSON list of image URLs
#     """
#     if not g.user:
#         return redirect(url_for('login'))
#     return getUserImages(g.user)

# @app.route('/user/profile')
# def getCurrentUserProfile():
#     if not g.user:
#         return redirect(url_for('login'))
#     return getUserProfile(g.user)

# @app.route('/getcurrentuser', methods=["GET"])
# def getCurrentUser():
#     """Gets current logged in user
#
#     Returns:
#         str: JSON object containing the current user
#     """
#     return jsonify({
#         'username': g.user
#     })

@app.route('/subscribe', methods=["POST"])
def subscribe():
    s = request.form.to_dict()['json_string']
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)

    group = d['groupID']
    subscribeGroup(g.user, group)
    return "None"


@app.route('/setFreetime', methods=["POST"])
def setFreetime():
    s = request.form.to_dict()['json_string']
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)

    freetime = d['freetime']
    updateFreetime(g.user, freetime)
    return "None"


@app.route('/addTask', methods=["POST"])
def addTask():
    s = request.form.to_dict()['json_string']
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)

    taskName = d['taskName']
    taskDuration = d['taskDuration']
    addTaskToDB(g.user, taskName, taskDuration)
    return "None"


@app.route('/fetchEvents', methods=["GET"])
def fetchEvents():
    return fetchEventsFromDB(g.user)


@app.route('/updateGoingStatus', methods=["POST"])
def updateGoingStatus():
    s = request.form.to_dict()['json_string']
    json_acceptable_string = s.replace("'", "\"")
    d = json.loads(json_acceptable_string)

    eventID = d['eventID']
    going = d['going']
    return updateGoingStatusToDB(g.user, eventID, going)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
