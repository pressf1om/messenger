import os
import traceback
import time
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
import sys
from pathlib import Path
import pygame
import requests
from bs4 import BeautifulSoup as BS
from pyowm import OWM
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import glob

server = 'http://127.0.0.1:5000'
cry = None
get_split = None
check_is_anonym = None
password_path = 'C:\\Messenger Files\\log.txt'
chat_file = 'C:\\Messenger Files\\history_message.txt'
device_path = 'C:\\Messenger Files\\device.txt'
dark, user, pword = False, '', ''
dirlist = None
count = None
path = None
dist = None
number_song = None
song = None
off = None
is_private = None
a, b = None, None
true_dialog = None
nickname_to = None
count_of_element = None
dist_of_create_btn = {}
s_dialogs_name_file_only = None
user_to = None
get_split2, get_split2_ = None, None
data_updates = f"C:\\Messenger Files\\updates.txt"
info_in_file_data_updates_open_r = None
dict_chats_user = {}
file__ = None
old_device = None
get_split____ = None
name_ = None
password_ = None
rem_ = None
open_window = None

try:
    device_file = open(device_path)
    device_file_read = device_file.read(1)
    if str(device_file_read) == '1':
        old_device = True
    elif str(device_file_read) == '0':
        old_device = False
    print(f'old_device = {old_device}')
except Exception as er_device_path:
    old_device = False
    print(f'old_device = {old_device}')
    print(er_device_path)


class MainWindow(QMainWindow):
    def __init__(self):
        global dist_of_create_btn, count_of_element, s_dialogs_name_file_only, file__, dict_chats_user
        super().__init__()
        uic.loadUi('./design/mainwindow/mainwindowchoosemeenu.ui', self)
        self.setWindowTitle('Messenger')
        self.setWindowIcon(QtGui.QIcon(f'design/mainwindow/icon.png'))
        self.music.clicked.connect(self.on_player)
        self.weather.clicked.connect(self.weatherf)
        self.covid.clicked.connect(self.covidf)
        self.add_dialog.clicked.connect(self.add_dialog_bt)
        self.vertical_layout_chats = QVBoxLayout(self)
        self.main_groupbox.setLayout(self.vertical_layout_chats)
        self.settings.clicked.connect(self.open_settings)

        counter = 0

        s_dialogs = []
        s_dialogs_name_file_only = []

        try:
            for result_dialog in glob.glob(f'C:\\Messenger Files\\accounts\\{user}\\dialogs\\*.txt'):
                counter += 1
                print(f'Dialog file found under №{counter}: {result_dialog}')
                file_ = (str(result_dialog)[result_dialog.find("_") + 1:-4]) + '.txt'
                file__ = (str(result_dialog)[result_dialog.find("_") + 1:-4])
                s_dialogs.append(file_)
                s_dialogs_name_file_only.append(file__)
        except:
            os.mkdir(f'C:\\Messenger Files\\accounts\\{user}\\dialogs\\')

        counter_create_start_btn = 0

        for k in s_dialogs_name_file_only:
            try:
                self.old_dialog_btn = QPushButton(s_dialogs_name_file_only[counter_create_start_btn])
                dist_of_create_btn[counter_create_start_btn] = s_dialogs_name_file_only[counter_create_start_btn]
                counter_create_start_btn += 1
                self.vertical_layout_chats.addWidget(self.old_dialog_btn)
                self.old_dialog_btn.clicked.connect(lambda ch, btn=self.old_dialog_btn: self.main_menu_dialog(btn))
                self.old_dialog_btn.setStyleSheet(
                    ".QPushButton {background-color:#ffffff;border-radius:25px;border:2px solid #dcdcdc;color:#666666;font-family:Arial;font-size:15px;font-weight:bold;}.QPushButton:hover {background-color:#f6f6f6;color:#121212;}.QPushButton:pressed {border-color:#121212;}")
            except:
                continue

        print(f"dict_chats_user = {dict_chats_user}")

        self.vertical_layout_chats.addStretch()

        count_of_element = self.vertical_layout_chats.count()

    def covidf(self):
        self.ex_5 = CovidInfo()
        self.ex_5.show()

    def weatherf(self):
        self.ex_6 = weather()
        self.ex_6.show()

    def on_player(self):
        self.ex_3 = MainWindowMusic()
        self.ex_3.show()

    def add_dialog_bt(self):
        newBtn = QPushButton('New dialog')
        newBtn.setStyleSheet(
            ".QPushButton {background-color:#ffffff;border-radius:25px;border:2px solid #dcdcdc;color:#666666;font-family:Arial;font-size:15px;font-weight:bold;}.QPushButton:hover {background-color:#f6f6f6;color:#121212;}.QPushButton:pressed {border-color:#121212;}")
        newBtn.clicked.connect(self.saveDialog)
        self.vertical_layout_chats.addWidget(newBtn)
        self.vertical_layout_chats.addStretch(1)

    def saveDialog(self):
        self.ex_7 = find_name_window()
        self.ex_7.show()

    def main_menu_dialog(self, btn):
        global user_to
        global dist_of_create_btn, s_dialogs_name_file_only

        print(dist_of_create_btn)
        user_to = btn.text()

        print(user_to)

        self.ex_main_window = MainDialogWindow()
        self.ex_main_window.show()

    def open_settings(self):
        self.ex_settings = Settings()
        self.ex_settings.show()


class find_name_window(QWidget):
    def __init__(self):
        super().__init__()
        find_name_window.setWindowTitle(self, 'Add dialog')
        self.setWindowIcon(QtGui.QIcon(f'design/mainwindow/icon.png'))
        self.check_Btn = QPushButton('Check')
        self.add_dialog = QPushButton('Add Dialog')
        self.add_Btn = QPushButton('Add dialog')
        self.check_Btn.setStyleSheet(
            ".QPushButton {background-color:#ffffff;border-radius:25px;border:2px solid #dcdcdc;color:#666666;font-family:Arial;font-size:15px;font-weight:bold;}.QPushButton:hover {background-color:#f6f6f6;color:#121212;}.QPushButton:pressed {border-color:#121212;}")
        self.add_dialog.setStyleSheet(
            ".QPushButton {background-color:#ffffff;border-radius:25px;border:2px solid #dcdcdc;color:#666666;font-family:Arial;font-size:15px;font-weight:bold;}.QPushButton:hover {background-color:#f6f6f6;color:#121212;}.QPushButton:pressed {border-color:#121212;}")
        self.setFixedSize(500, 280)
        self.layout = QGridLayout(self)
        self.groupBox = QGroupBox(self)
        self.groupBox.setLayout(self.layout)
        self.groupBox.setGeometry(QRect(40, 20, 421, 231))
        self.line_nickname = QLineEdit(self.groupBox)
        self.line_nickname.setGeometry(QRect(160, 30, 150, 20))
        self.line_nickname.setStyleSheet(
            ".QLineEdit {background-color:#ffffff;border-radius:25px;border:2px solid #dcdcdc;color:#666666;font-family:Bebas Neue;font-size:17px;}")
        self.label_check = QLabel('', self.groupBox)
        self.label_check.setGeometry(QRect(130, 97, 170, 35))
        self.label_check_ = QLabel('', self.groupBox)
        self.label_check_.setGeometry(QRect(130, 180, 170, 35))
        label_nickname = QLabel('Nickname: ', self.groupBox)
        label_nickname.setGeometry(QRect(100, 30, 150, 20))
        self.check_Btn.clicked.connect(self.check_nickname)
        self.layout.addWidget(self.check_Btn)
        self.add_dialog.clicked.connect(self.create_dialog)
        self.layout.addWidget(self.add_dialog)

    def check_nickname(self):
        global a, b, true_dialog, nickname_to, server
        try:
            URL = f'{server}/oll_nicknames'
            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
            }

            req = requests.get(URL, headers=HEADERS)
            soup = BS(req.content, 'html.parser')
            amounts = soup.find_all('div', class_='users')

            for i in amounts:
                a = (i.get_text())
                b = (a.split())

            nickname_to = self.line_nickname.text()

            print(nickname_to)
            print(str(b))

            if str(nickname_to) in str(b):
                self.label_check.setStyleSheet("background-color: #2e9e32")
                true_dialog = 1
            else:
                self.label_check.setStyleSheet("background-color: #ed1515")
                true_dialog = 0
        except:
            pass

    def create_dialog(self):
        global true_dialog, nickname_to, user, dict_chats_user, server
        print(1111111111)
        print(dict_chats_user)
        if true_dialog == 1:
            try:
                # have not dir
                os.makedirs(f'C:\\Messenger Files\\accounts\\{user}\\dialogs\\')
                data_dialog_path = f"C:\\Messenger Files\\accounts\\{user}\\dialogs\\d_{nickname_to}.txt"
                data_dialog_path_open = open(data_dialog_path, 'w')
                data_dialog_path_open.write(f"{nickname_to}")
                print(f'user: {user}, nickname_to: {nickname_to}')
                requests.post(f'{server}/get_chats', json={'who_chat': user, 'with_who_chat': nickname_to})
                # requests.post(f'http://127.0.0.1:5000/get_chats/{user}', json={'who_chat': user, 'with_who_chat': nickname_to})
                # requests.post('http://127.0.0.1:5000/get_chats', json={'chats': dict_chats_user})
                self.label_check_.setStyleSheet("background-color: #2e9e32")
            except:
                # have dir
                data_dialog_path = f"C:\\Messenger Files\\accounts\\{user}\\dialogs\\d_{nickname_to}.txt"
                data_dialog_path_open = open(data_dialog_path, 'w')
                data_dialog_path_open.write(f"{nickname_to}")
                print(f'user: {user}, nickname_to: {nickname_to}')
                requests.post(f'{server}/get_chats', json={'who_chat': user, 'with_who_chat': nickname_to})
                # requests.post(f'http://127.0.0.1:5000/get_chats/{user}', json={'who_chat': user, 'with_who_chat': nickname_to})
                # requests.post('http://127.0.0.1:5000/get_chats', json={'chats': dict_chats_user})
                self.label_check_.setStyleSheet("background-color: #2e9e32")
        else:
            self.label_check_.setStyleSheet("background-color: #ed1515")


class Settings(QMainWindow):
    def __init__(self):
        global info_in_file_data_updates_open_r
        super().__init__()
        uic.loadUi('./design/settings/settings.ui', self)
        Settings.setWindowTitle(self, 'Settings')
        self.setWindowIcon(QtGui.QIcon(f'design/settings/icon.png'))
        self.label_login.setText(user)
        self.label_password.setText(pword)
        self.check_update.clicked.connect(self.check_update_)
        try:
            data_updates_open_r = open(data_updates)
            info_in_file_data_updates_open_r = data_updates_open_r.read()
        except:
            data_updates_open_r = open(data_updates, 'w')
            info_in_file_data_updates_open_r = data_updates_open_r.write('0')
        self.version_of_client.setText(f'{info_in_file_data_updates_open_r}')

    def check_update_(self):
        global get_split2, get_split2_, data_updates, info_in_file_data_updates_open_r
        try:
            URL = f'{server}/desctop-update-check-for-dev'
            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
            }

            req = requests.get(URL, headers=HEADERS)
            soup = BS(req.content, 'html.parser')
            amounts = soup.find_all('div', class_='updates_desctop_client')

            for i in amounts:
                get_split2 = (i.get_text())
                get_split2_ = (get_split2.split())

            print(get_split2_)

            try:
                data_updates_open_r = open(data_updates)
                info_in_file_data_updates_open_r = data_updates_open_r.read()
                print(f'info_in_files update parse: {get_split2_}')
                print(f'info_in_files update file: {info_in_file_data_updates_open_r}')
            except:
                # make file
                pass

            print(f'{get_split2_}')
            print(info_in_file_data_updates_open_r)

            if info_in_file_data_updates_open_r != get_split2_[-1][1]:
                # update
                self.label_print_info_update.setText('There is a new update.')
                self.label_link_update.setText(f'Check out the update here: {server}/desctop-update-check.')
                self.version_of_client.setText(f'{get_split2_[-1][1]}')
                data_updates_open = open(data_updates, 'w')
                data_updates_open.write(f"{get_split2_[-1][1]}")
            else:
                self.label_print_info_update.setText('You have the latest version.')
                self.label_link_update.setText('')

        except:
            pass


def get_dta():
    try:
        password_path_open = open(password_path)
        info_in_file = password_path_open.readlines()
        if len(info_in_file) != 3 or info_in_file[1].rstrip() == '' \
                or info_in_file[0].rstrip() == '':
            return None
        else:
            return info_in_file
    except:
        return None


def wrt_dta(name='', password='', rem='False'):
    data = [name + '\n', password + '\n', rem]
    try:
        os.mkdir('C:\\Messenger Files\\')
    except:
        pass
    password_path_open = open(password_path, 'w')
    password_path_open.write(''.join(data))


class MainDialogWindow(QMainWindow):
    def __init__(self):
        global user_to
        global dist_of_create_btn, count_of_element
        super().__init__()
        uic.loadUi('./design/mainwindow/mainwindowchat.ui', self)
        self.sen_mes.clicked.connect(self.send)
        self.setWindowTitle('Messenger')
        self.setWindowIcon(QtGui.QIcon(f'design/mainwindow/icon.png'))
        self.after = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.get)
        self.timer.start(2000)
        self.music.clicked.connect(self.on_player)
        self.weather.clicked.connect(self.weatherf)
        self.covid.clicked.connect(self.covidf)
        self.label_message_to.setText(user_to)

    def covidf(self):
        self.ex_5 = CovidInfo()
        self.ex_5.show()

    def weatherf(self):
        self.ex_6 = weather()
        self.ex_6.show()

    def on_player(self):
        self.ex_3 = MainWindowMusic()
        self.ex_3.show()

    def get(self):
        try:
            req = requests.get(f'{server}/get_message', params={'after': self.after})
            if req.status_code == 200:
                global get_split
                messages = req.json()['messages']
                if 1 == 1:
                    if get_split[2] == 'F':
                        for m in messages:
                            if m['text'] != '':
                                self.pprint_mes.append('')
                                self.after = m['time']
                                if user == m['message_to'] and user_to == m['autor'] or user == m[
                                    'autor'] and user_to == m['message_to']:
                                    self.pprint_mes.append(f"|{time.asctime()}|--|{m['autor']}|:")
                                    self.pprint_mes.append(f"{m['text']}")

                                    # toastNotifier = win10toast.ToastNotifier()
                                    # toastNotifier.show_toast(f"{m['autor']}", f"{m['text']}")
                                else:
                                    pass
                            else:
                                self.pprint_mes.append('')
                                self.pprint_mes.append("You can't send empty messages!")
                                self.pprint_mes.append('')
                                self.label_2.setText("Status: |ERROR|")
                    else:
                        pass
                else:
                    pass
            else:
                pass
        except:
            return

    def send(self):
        global user_to
        text = self.input_mes.toPlainText()

        print(text)
        print(f'user: {user}')
        print(f'user_to: {user_to}')

        if text != '':
            requests.post(f'{server}/send_message', json={'text': text,
                                                          'autor': user,
                                                          'password': pword,
                                                          'message_to': user_to})

            self.label_2.setText("Status: |was sent|")
            self.input_mes.clear()
        else:
            self.pprint_mes.append('')
            self.pprint_mes.append("You can't send empty messages!")
            self.pprint_mes.append('')
            self.label_2.setText("Status: |ERROR|")


class MainLog(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('./design/login/login.ui', self)
        self.setWindowTitle('Login')
        self.setWindowIcon(QtGui.QIcon('design/login/icon.png'))
        if get_dta() is None:
            wrt_dta()
        else:
            if get_dta()[2] == 'True':
                self.input_name.setText(get_dta()[0].rstrip())
                self.input_password.setText(get_dta()[1].rstrip())
                self.radioButton.setChecked(True)
            else:
                wrt_dta()
        self.check_data.clicked.connect(self.check)

    def check(self):
        global get_split, user, pword
        global get_split____, name_, password_, rem_, open_window
        try:
            name_ = self.input_name.text()
            password_ = self.input_password.text()
            rem_ = self.radioButton.isChecked()

            print(name_)
            print(password_)
            print(rem_)

            # ONLINE = 'JOINED THE SERVER'

            requests.post(f'{server}/send_message',
                          json={'autor': name_, 'password': password_})

            try:
                URL = f'{server}/check-answer'
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

            except Exception:
                self.reg_info.setText("Login: |SeEr|")
                self.reg_info.setAlignment(Qt.AlignCenter)
        except:
            self.reg_info.setText("Login: |No connection required|")

        try:
            if get_split[2] == 'T':
                # wrong
                self.reg_info.setText("Login: |LogError|")
                self.reg_info.setAlignment(Qt.AlignCenter)
            else:
                # success
                # requests.post(f'http://127.0.0.1:5000/online', json={'username': user, 'online': datetime.datetime.now, 'status': "online"})
                if old_device:
                    user, pword = name_, password_
                    wrt_dta(name_, password_, str(rem_))
                    self.hide()
                    self.ex = MainWindow()
                    self.ex.show()
                else:
                    print('this is new device')

                    # response for make 2fa
                    requests.post(f'{server}/2fa_generate', json={'username_for_check': name_})

                    # get number from mail
                    # code_mail = input('Enter email code: ')
                    # requests.post(f'{server}/check_2fa', json={'code_from_email': code_mail})
                    self.hide()
                    self.ex_fa2 = fa2()
                    self.ex_fa2.show()
            return '1'
        except:
            pass


class fa2(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./design/2fa/code_check.ui', self)
        self.setWindowTitle('2FA')
        self.setWindowIcon(QtGui.QIcon(f'design/settings/icon.png'))
        self.check_code.clicked.connect(self.check_code_)

    def check_code_(self):
        global get_split, user, pword
        global get_split____, name_, password_, rem_, open_window

        # make flag for checking after
        open_device_path = open(device_path, 'w')

        code_text = self.code_input.text()

        print(f'code_text: {code_text}')

        if code_text != '':
            requests.post(f'{server}/check_2fa', json={'code_from_email': code_text})

        # parse and check result
        try:
            URL = f'{server}/check_2fa'
            HEADERS = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                              ' AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
            }

            req = requests.get(URL, headers=HEADERS)
            soup = BS(req.content, 'html.parser')
            amounts = soup.find_all('div', class_='check')

            for i in amounts:
                get___ = (i.get_text())
                get_split____ = (get___.split())

        except Exception:
            print('Parsing error')

        print(f'get_split____[0] = {get_split____[0]}')

        if str(get_split____[0]) == 'True':
            open_window = 1
        elif str(get_split____[0]) == 'False':
            open_window = 0

        print(f'open_window: {open_window}')

        if open_window == 1:
            # suc
            open_device_path.write('1')
            user, pword = name_, password_
            wrt_dta(name_, password_, str(rem_))
            self.status_code.setText('Ok')
            self.hide()
            self.ex = MainWindow()
            self.ex.show()
        elif open_window == 0:
            # wrong
            self.status_code.setText('Oops! The code from the message is incorrect!')
            self.code_input.setText('')
            open_device_path.write('0')
            print('no open')


class weather(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./design/weather/weather.ui', self)
        self.setWindowTitle('Weather')
        self.setWindowIcon(QtGui.QIcon('design/weather/icon.png'))
        self.pushButton.clicked.connect(self.check_weather)

    def check_weather(self):
        place = self.lineEdit.text()
        print(place)

        owm = OWM('067068fb5d14689ed3260ff50228a8c8')
        mgr = owm.weather_manager()
        try:
            observation = mgr.weather_at_place(place)
            w = observation.weather

            temp = w.temperature('celsius')
            wind = w.wind()
            main_weather = w.detailed_status
            humidity = w.humidity

            self.pprint_text.append("In city " + place + ":")
            self.pprint_text.append(str('Temperature: ' + str(temp['temp'])))
            self.pprint_text.append(str('Wind: ' + str(wind['speed']) + "М\с"))
            self.pprint_text.append(str('Now: ' + str(main_weather)))
            self.pprint_text.append(str('Humidity: ' + str(humidity) + "%"))
            self.pprint_text.append('')
        except:
            self.pprint_text.append("OOPS! ERROR!")
            self.pprint_text.append('')


class CovidInfo(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./design/covid/covid.ui', self)
        self.setWindowTitle('Covid-19')
        self.setWindowIcon(QtGui.QIcon('design/covid/icon.png'))
        self.pushButton.clicked.connect(self.parse_mode)

    def parse_mode(self):
        URL = 'https://www.worldometers.info/coronavirus/'
        HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko)'
                          ' Chrome/80.0.3987.116 Safari/537.36 OPR/67.0.3575.130'
        }

        r = requests.get(URL, headers=HEADERS)
        soup = BS(r.content, 'html.parser')
        amounts = soup.find_all('div', class_='maincounter-number')
        spisok = []

        for i in amounts:
            spisok.append(*(i.get_text().split()))

        self.label_2.setText(f'Total fall ill: {spisok[0]}')
        self.label_3.setText(f'Total died: {spisok[1]}')
        self.label_4.setText(f'Total recovered: {spisok[2]}')
        self.label_2.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.label_3.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.label_4.setFont(QtGui.QFont("Times", 25, QtGui.QFont.Bold))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4.setAlignment(Qt.AlignCenter)


class MainWindowMusic(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./design/mainmusic/mainmusic.ui', self)
        self.setWindowTitle('Player')
        self.setWindowIcon(QtGui.QIcon(f'design/mainmusic/icon.png'))
        self.chooseTrackbt.clicked.connect(self.getDirectory)
        self.scan.clicked.connect(self.find_files)
        self.onBT.clicked.connect(self.on_music)
        self.offBT_4.clicked.connect(self.off_music)

    def getDirectory(self):
        global dirlist
        dirlist = QFileDialog.getExistingDirectory(self, "/", "/")
        print(dirlist)
        self.pprint_text.append(f"|Selected a folder: {dirlist}|")

    def find_files(self):
        global count
        count = 0
        global path
        path = Path(str(dirlist) + '/')
        self.pprint_text.clear()
        self.pprint_text.append(f'We are in the folder {dirlist}')

        global dist
        dist = {}

        for result in path.glob('*.mp3'):
            count += 1
            self.pprint_text.append(f'Audio file found under №{count}: {result}')
            dist[f'{count}'] = result
        print(dist)

    def on_music(self):
        global number_song
        number_song = self.inputN.text()
        global song
        pygame.mixer.init()
        song = pygame.mixer.music.load(f'{dist[number_song]}')
        global on
        on = pygame.mixer.music.play()
        print(f'{path}/{number_song}.mp3')
        self.inputN.setText('')

    def off_music(self):
        global off
        off = pygame.mixer.music.stop()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex5 = MainLog()
    ex5.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
