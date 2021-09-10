import os
import pyotp
import random
from flask import Flask, Response, request, render_template
from time import time
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.utils import redirect
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import sqlalchemy
import itsdangerous

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mes.sqlite'
app.config['SECRET_KEY'] = 'qc_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
confirmation_tool = itsdangerous.URLSafeTimedSerializer("qc_secret_key")

host = '127.0.0.1:5000'
is_anonym = None
message_history = []
oll_chats = {}
oll_chats_ = {}
email_to = None
s = []
email_from = "QC-welcome@yandex.ru"
password_email = "742834782347823746278109201284210"
email_confirmation = "QC-email-confirmation@yandex.ru"
password_email_confirmation = "742834782347823746278109201284210"
username = None
password = None
email = None
token = None
email_user = None
email_2fa = 'QC-2fa@yandex.ru'
password_email_2fa = '742834782347823746278109201284210'
number = None
hotp = None
result_ver = None


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


class News(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    updates_desctop_client = db.Column(db.String(200), nullable=False)
    updates_desctop_client_date_time = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    disc_of_update = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(200), nullable=False)


class Dialogs(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    dialogs_with = db.Column(db.String, nullable=True)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/home')
def home_main():
    return render_template("home.html")


@app.route('/send_message', methods=['POST', 'GET'])
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return Response({'ok': False}, 400)

    global is_anonym
    print(is_anonym)

    text = data.get('text')
    autor = data.get('autor')
    password = data.get('password')
    message_to = data.get('message_to')

    for local_users_data in User.query.all():
        uu = local_users_data.__dict__
        print('-------------------------')
        print(f"ID: {uu['id']}")
        print(f"EMAIL: {uu['email']}")
        print(f"USERNAME: {uu['username']}")
        print(f"PASSWORD: {uu['password']}")
        print('-------------------------')

    for jj in User.query.order_by(User.id):
        u = jj.__dict__
        if autor in u['username']:
            if autor == u['username']:
                if password == u['password']:
                    is_anonym = 0
                    print(autor)
                    print(u['username'])
                    print()
                    print('r')
                    print()
                    print()
                    print(password)
                    print(u['password'])
                    break
                elif password != u['password']:
                    is_anonym = 1
                    print(autor)
                    print(u['username'])
                    print()
                    print('f')
                    print()
                    print()
                    print(password)
                    print(u['password'])
            else:
                is_anonym = 1
                print('gg')
        else:
            print()
            print()
            print()
            print()
            print()
            print()
            print(autor)
            print(u['username'])
            print()
            print()
            print()
            print()
            print(password)
            print(u['password'])
            print()
            print()
            print()
            print()
            print()
            print()
            is_anonym = 1

    if (autor and text) is not None:
        message_history.append({
            'text': text,
            'autor': autor,
            'time': time(),
            'password': password,
            'message_to': message_to,
        })
        #

    return Response({'ok': True})


@app.route('/get_message')
def get_message():
    after = request.args.get('after', '0')

    try:
        new_after = float(after)
    except:
        return Response({'ok': False})

    new = [me for me in message_history if float(me['time']) > new_after]
    return {'messages': new}


@app.route("/login/reg", methods=['POST', 'GET'])
def reg():
    global email_to
    global email_from
    global password_email
    global username
    global password
    global email
    global email_confirmation
    global password_email_confirmation
    global token

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        token = confirmation_tool.dumps(email, salt='email-confirm')

        message_confirm = MIMEMultipart()
        message_confirm['From'] = email_confirmation
        message_confirm['To'] = email
        message_confirm['Subject'] = 'Confirmation.'

        body = f"Hi! You have started registering in the QC messenger. \nTo confirm your email and complete the registration, follow the link: http://{host}/email-confirmation/{token}. \nIf it wasn't you, just ignore this message. \nSincerely yours, QC team =)"
        message_confirm.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(email_confirmation, password_email_confirmation)
        server.send_message(message_confirm)
        server.quit()

        return render_template("email.html")
    else:
        return render_template("reg.html")


@app.route("/email-confirmation/<token>", methods=['POST', 'GET'])
def confirmation(token):

    global username
    global password
    global email

    try:
        email_ = confirmation_tool.loads(token, salt='email-confirm', max_age=120)

        try:
            user_man = User(username=username, password=password, email=email)

            message = MIMEMultipart()
            message['From'] = email_from
            message['To'] = email
            message['Subject'] = 'Your username and password.'

            body = f"Your login details: \nLogin: {username}\nPassword: {password}\nEmail address to which the registration was made: {email}\nTechnical Support email: QC-help-online@yandex.ru\nThank you for registering, good luck using it!\nSincerely, your QC =)"
            message.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
            server.login(email_from, password_email)

            db.session.add(user_man)
            db.session.commit()

            server.send_message(message)
            server.quit()

            return redirect('/successful_registration')
        except Exception as r:
            print(r)
            return "Error(("

    except:
        return render_template("email_bad.html")

    return "1"


@app.route("/admin-for-dev", methods=['POST', 'GET'])
def admin():
    return render_template("admin.html")


@app.route("/admin-for-dev/users")
def printuser():
    userprint = User.query.order_by(User.id).all()
    return render_template("adminuser.html", data=userprint)


@app.route("/admin-for-dev/add_updates", methods=['POST', 'GET'])
def add_updates():
    if request.method == "POST":
        update_desctop_client = request.form['update_desctop_client']
        disc_of_update = request.form['disc_of_update']
        link = request.form['link']
        update_desctop_client = News(updates_desctop_client=update_desctop_client, disc_of_update=disc_of_update,
                                     link=link)

        try:
            db.session.add(update_desctop_client)
            db.session.commit()
            return redirect('/desctop-update-check')
        except Exception as exc:
            print(exc)
            return "Error(("
    else:
        return render_template("add_updates.html")


@app.route("/sup")
def sup():
    return render_template("support.html")


@app.route("/check-answer")
def answer():
    global is_anonym
    is_anonym1 = str(is_anonym)
    print(is_anonym)
    if is_anonym1 == '0':
        return render_template("check_sus.html")
    elif is_anonym1 == '1':
        return render_template("check_fail.html")
    else:
        return is_anonym1


@app.route("/download")
def down():
    return render_template("download.html")


@app.route("/oll_nicknames")
def return_nicknames():
    username_print = User.query.order_by(User.username).all()
    return render_template("oll_users.html", data=username_print)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/successful_registration")
def sus():
    return render_template("sus.html")


@app.route("/desctop-update-check-for-dev")
def check_desctop_up_for_dev():
    update_print = News.query.order_by(News.updates_desctop_client).all()
    return render_template("update_desctop.html", data=update_print)


@app.route("/desctop-update-check")
def check_desctop_up():
    update_print_for_users = News.query.order_by(News.updates_desctop_client, News.id,
                                                 News.updates_desctop_client_date_time, News.disc_of_update,
                                                 News.link).all()
    return render_template("update_desctop_for_users.html", data=update_print_for_users)


@app.route('/get_chats', methods=['POST', 'GET'])
def get_chats():
    global s
    if request.method == "POST":
        data = request.json

        print(f"data = {data}")
        print(type(data))

        who_chat = data.get('who_chat')
        with_who_chat = data.get('with_who_chat')

        print(f'who_chat = {who_chat}')
        print(f'with_who_chat = {with_who_chat}')

        if with_who_chat not in Dialogs.query.order_by(Dialogs.username, Dialogs.dialogs_with):
            user_dialogs = Dialogs(username=who_chat, dialogs_with=with_who_chat)
            try:
                db.session.add(user_dialogs)
                db.session.commit()
                return redirect('/')
            except Exception as exc:
                print(exc)
                return "Error(("

    else:
        pprint_chats = Dialogs.query.order_by(Dialogs.username, Dialogs.dialogs_with).all()
        return render_template("pprint_user_dialogs.html", data=pprint_chats)


@app.route('/print_chats/<nickname>', methods=['POST', 'GET'])
def print_chats(nickname):
    if request.method == "GET":
        pprint_chats = Dialogs.query.order_by(Dialogs.dialogs_with).filter(Dialogs.username == nickname)
        return render_template("pprint_user_dialogs.html", data=pprint_chats)
    else:
        return "POST"


@app.route("/description")
def description():
    return render_template("description.html")


@app.route("/2fa_generate", methods=['POST', 'GET'])
def func_2fa():
    global email_user
    global number
    global hotp
    if request.method == "POST":
        # get oll data
        data_2fa = request.json

        # get username
        username_for_check = data_2fa.get('username_for_check')
        print(f'username_for_check: {username_for_check}')

        # get email user
        for yyy in User.query.order_by(User.email):
            yyyy = yyy.__dict__
            # print('-------------------------')
            # print(f"EMAIL: {yyyy['email']}")
            # print(f"USERNAME: {yyyy['username']}")
            # print('-------------------------')
            if yyyy['username'] == username_for_check:
                email_user = yyyy['email']
                break

        print(f'email_user: {email_user}')

        # generate key
        key = pyotp.random_base32()
        hotp = pyotp.HOTP(key)
        print(f'key: {key}')

        # generate number
        number = random.randint(0, 100000000000000000000000)
        print(f'number: {number}')

        # generate message
        mes_2fa = hotp.at(number)

        message = MIMEMultipart()
        message['From'] = email_2fa
        message['To'] = email_user
        message['Subject'] = 'Confirm login.'

        body = f"Someone is trying to log in to your account from a new device.\nIf you want to log in to your account on a new device, enter the code: {mes_2fa}.\nIf you don't do it:\n1. Change your password immediately.\n2. If you encounter any difficulties, write a letter to support: QC-help-online@yandex.ru."
        message.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(email_2fa, password_email_2fa)

        # send message
        server.send_message(message)
        server.quit()

        print(f'mes_2fa: {mes_2fa}')

        return render_template("2fa_gen.html", data=email_user)
    else:
        return render_template("2fa_gen.html", data=email_user)


@app.route("/check_2fa",  methods=['POST', 'GET'])
def check_2fa():
    global result_ver
    global hotp
    global number
    if request.method == "POST":
        # get code
        data_2fa_check = request.json

        # get username
        code_from_mail = data_2fa_check.get('code_from_email')
        print(f'code_from_mail: {code_from_mail}')

        # verify
        result_ver = hotp.verify(code_from_mail, number)
        if result_ver:
            print(result_ver)
            print('code is right')
        else:
            print('code is false')

        return render_template("check_2fa.html", data=result_ver)
    else:
        return render_template("check_2fa.html", data=result_ver)


if __name__ == '__main__':
    # port = int(os.environ.get("PORT", 5000))
    # app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=5000)
