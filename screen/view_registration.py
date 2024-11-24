import sqlite3
from screen.view_login import LoginScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from hashlib import sha256
from functools import partial

class RegistrationScreen(LoginScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.username = TextInput(hint_text='Имя пользователя', multiline=False)
        self.password = TextInput(hint_text='Пароль', multiline=False, password=True)
        self.secret_question = TextInput(hint_text='Секретный вопрос', multiline=False)
        self.secret_answer = TextInput(hint_text='Ответ на секретный вопрос', multiline=False)

        register_button = Button(text='Зарегистрироваться', on_press=self.register)
        back_button = Button(text='Назад', on_press=partial(self.change_screen, 'login'))

        layout.add_widget(Label(text='Регистрация'))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.secret_question)
        layout.add_widget(self.secret_answer)
        layout.add_widget(register_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def register(self, instance):
        username = self.username.text
        password = sha256(self.password.text.encode()).hexdigest()
        secret_question = self.secret_question.text
        secret_answer = self.secret_answer.text

        conn = sqlite3.connect("../poplaukhin_db.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, password, role, secret_question, secret_answer)
                VALUES (?, ?, 'user', ?, ?)
            """, (username, password, secret_question, secret_answer))
            conn.commit()
            self.manager.current = 'login'
        except sqlite3.IntegrityError:
            self.add_widget(Label(text='Пользователь уже существует!'))
        finally:
            conn.close()

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name