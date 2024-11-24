import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from hashlib import sha256
from functools import partial

class PasswordRecoveryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.username = TextInput(hint_text='Имя пользователя', multiline=False)
        self.secret_question = Label(text='Секретный вопрос:')
        self.secret_answer = TextInput(hint_text='Ответ на секретный вопрос', multiline=False)
        self.new_password = TextInput(hint_text='Новый пароль', multiline=False, password=True)

        recovery_button = Button(text='Восстановить пароль', on_press=self.recover_password)
        back_button = Button(text='Назад', on_press=partial(self.change_screen, 'login'))

        layout.add_widget(Label(text='Восстановление пароля'))
        layout.add_widget(self.username)
        layout.add_widget(self.secret_question)
        layout.add_widget(self.secret_answer)
        layout.add_widget(self.new_password)
        layout.add_widget(recovery_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def recover_password(self, instance):
        username = self.username.text
        answer = self.secret_answer.text
        new_password = sha256(self.new_password.text.encode()).hexdigest()

        conn = sqlite3.connect("../poplaukhin_db.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT secret_question, secret_answer FROM users WHERE username=?
        """, (username,))
        user = cursor.fetchone()

        if user and user[1] == answer:
            cursor.execute("""
                UPDATE users SET password=? WHERE username=?
            """, (new_password, username))
            conn.commit()
            self.manager.current = 'login'
        else:
            self.add_widget(Label(text='Неверный ответ на секретный вопрос!'))
        conn.close()

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name