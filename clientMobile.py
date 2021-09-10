# CHECK IT PLS
"""Attention! This client is not yet operational. Active development is underway. This is not available yet((("""
from flask import Flask, Response, request, render_template, redirect
import requests
from bs4 import BeautifulSoup as BS
from threading import Thread
import time
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.utils import redirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import sqlalchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.sqlite'
app.config['SECRET_KEY'] = 'qc_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

is_auth = None
name_auth = None
get_split = None
name_auth_ = None
get_split2__ = None
after = 0
messages_ = []


class Messages(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    topic_of_dialog = db.Column(db.String, nullable=True)
    text = db.Column(db.String, nullable=True)


@app.route('/', methods=['POST', 'GET'])
def login():
    global get_split, is_auth, name_auth, name_auth_
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']

        requests.post('http://127.0.0.1:5000/send_message',
                      json={'autor': username, 'password': password})

        try:
            URL = 'http://127.0.0.1:5000/check-answer'
            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
            }

            req = requests.get(URL, headers=HEADERS)
            soup = BS(req.content, 'html.parser')
            amounts = soup.find_all('div', class_='check')

            for i in amounts:
                get_ = (i.get_text())
                get_split = (get_.split())

        except Exception as er:
            print(er)

        print(get_split)

        if get_split[2] == 'T':
            # wrong
            is_auth = 0
            name_auth = None
            return render_template("unsuc.html")
        else:
            # suc
            is_auth = 1
            name_auth = username
            name_auth_ = username
            return redirect('/main')
    else:
        return render_template("mobile_login.html")


@app.route('/main', methods=['POST', 'GET'])
def main_mobile():
    global is_auth, name_auth
    if is_auth == 1:
        # suc
        return render_template("mobile_main.html", name_auth=name_auth)
        # wrong
    elif is_auth == 0:
        return render_template("unsuc.html")


# depends on the number of friends added to the c pk version
@app.route('/dialogs/<name_auth>', methods=['POST', 'GET'])
def dialogs(name_auth):
    global is_auth, name_auth_, get_split2__
    if is_auth == 1:
        # suc
        try:
            URL = f'http://127.0.0.1:5000/print_chats/{name_auth}'
            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
            }

            req = requests.get(URL, headers=HEADERS)
            soup = BS(req.content, 'html.parser')
            amounts = soup.find_all('div', class_='dialogs')

            for i in amounts:
                get_split2_ = (i.get_text())
                get_split2__ = (get_split2_.split())
                # return get_split2__

        except Exception as errrror:
            print(errrror)

        return render_template("dialogs.html", name_auth=name_auth, name_auth_=name_auth_, get_split2__=get_split2__)
    elif is_auth == 0:
        # wrong
        return render_template("unsuc.html")


error_with_practices = """
@app.route('/dialogs/<name_auth>/<name_person_dialog>', methods=['POST', 'GET'])
def dialog_with_person(name_auth, name_person_dialog):
    global is_auth, after
    if is_auth == 1:
        while True:
            try:
                req = requests.get('http://127.0.0.1:5000/get_message', params={'after': after})
                if req.status_code == 200:
                    messages = req.json()['messages']
                    if is_auth == 1:
                        for m in messages:
                            if m['text'] != '':
                                after = m['time']
                                print(after)
                                if (name_auth == m['message_to'] and name_person_dialog == m['autor']) or (name_auth == m['autor'] and name_person_dialog == m['message_to']):
                                    # print
                                    topic_of_dialog_ = f"|PRIVATE MESSAGE FROM: {m['autor']}|-|TO: {m['message_to']}|-|{time.asctime()}| (ONLINE)"
                                    text_ = f"{m['text']}"
                                    add_messages = Messages(username=name_auth, text=text_, topic_of_dialog=topic_of_dialog_)  # topic_of_dialog=topic_of_dialog
                                    # old_messages = Messages.query.order_by(Messages.username, Messages.text, Messages.topic_of_dialog).all()
                                    for yyy in User.query.order_by(Messages.topic_of_dialog, Messages.text):
                                        yyyy = yyy.__dict__
                                        # print('-------------------------')
                                        # print(f"EMAIL: {yyyy['email']}")
                                        # print(f"USERNAME: {yyyy['username']}")
                                        # print('-------------------------')
                                        if yyyy['username'] == str(name_auth):
                                            print('yes')
                                            break

                                    print(name_auth)
                                    print(text_)
                                    print(topic_of_dialog_)

                                    try:
                                        if (topic_of_dialog_ and text_) not in Messages.query.order_by(Messages.topic_of_dialog, Messages.text).filter(Messages.username == name_auth):  # Messages.text != text_ and Messages.topic_of_dialog != topic_of_dialog_ and Messages.username != name_auth
                                            db.session.add(add_messages)
                                            db.session.commit()
                                            pprint_messages = Messages.query.order_by(Messages.text).filter(Messages.username == name_auth)
                                            return render_template("dialog_with_person.html", data=pprint_messages)
                                        else:
                                            pprint_messages = Messages.query.order_by(Messages.text).filter(Messages.username == name_auth)
                                            return render_template("dialog_with_person.html", data=pprint_messages)
                                    except Exception as exc:
                                        print(exc)
                                        return "Error(("
                                else:
                                    return render_template("error_get_message.html", name_auth=name_auth, name_person_dialog=name_person_dialog, message_to=m['message_to'], autor=m['autor'])
                            else:
                                return "error 2"
                    else:
                        return "error 3"
                else:
                    return "error 4"
            except Exception as errrrrrrrrrrrrrrrrooor:
                print(errrrrrrrrrrrrrrrrooor)
                return "except" 
        # return render_template("dialog_with_person.html", req=req)
    elif is_auth == 0:
        # wrong
        return render_template("unsuc.html")
"""

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
