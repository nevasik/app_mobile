import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from hashlib import sha256
from functools import partial

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.username = TextInput(hint_text='Имя пользователя', multiline=False)
        self.password = TextInput(hint_text='Пароль', multiline=False, password=True)
        login_button = Button(text='Войти', on_press=self.login)
        register_button = Button(text='Создать аккаунт', on_press=partial(self.change_screen, 'registration'))

        layout.add_widget(Label(text='Авторизация'))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_button)
        layout.add_widget(register_button)

        self.add_widget(layout)

    def login(self, instance):
        username = self.username.text
        password = sha256(self.password.text.encode()).hexdigest()

        conn = sqlite3.connect("../poplaukhin_db.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            if user[0] == 'admin':
                self.manager.current = 'admin_screen'
            else:
                self.manager.current = 'user_screen'
        else:
            self.username.text = ''
            self.password.text = ''
            self.add_widget(Label(text='Неверные данные!'))

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
