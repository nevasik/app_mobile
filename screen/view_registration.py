import sqlite3

from database.database import get_db_path
from screen.view_login import LoginScreen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from hashlib import sha256
from functools import partial

class RegistrationScreen(LoginScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.background = Image(
            source='/Users/mac/PycharmProjects/app_poplaukhin/static/background.jpg',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1)
        )

        self.username = TextInput(
            hint_text='Имя пользователя',
            multiline=False,
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'y': 0.657}
        )

        self.password = TextInput(
            hint_text='Пароль',
            multiline=False,
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'y': 0.657},
            password=True
        )

        self.secret_question = TextInput(
            hint_text='Секретный вопрос',
            multiline=False,
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'y': 0.657},
        )

        self.secret_answer = TextInput(
            hint_text='Ответ',
            multiline=False,
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'y': 0.657},
        )

        self.error_label = Label(
            text='', color=(1, 0, 0, 1)
        )

        register_button = Button(
            text='Зарегистрироваться',
            size_hint=(0.5, 0.1),  # Кнопка займет 50% ширины и 10% высоты родителя
            pos_hint={'center_x': 0.5},  # Выравнивание по центру
            background_color=(0, 0.5, 0.7, 1),
            on_press=self.register,
        )

        back_button = Button(
            text='Назад',
            size_hint=(0.3, 0.1),  # 30% ширины, 10% высоты
            pos_hint={'center_x': 0.5},  # Центрирование по оси X
            background_color=(0.2, 0.7, 0.2, 1),
            on_press=partial(self.change_screen, 'login'),
        )

        self.add_widget(self.background)
        layout.add_widget(Label(
            text='Регистрация',
            color=(0, 0, 0, 1)
        ))
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(self.secret_question)
        layout.add_widget(self.secret_answer)
        layout.add_widget(register_button)
        layout.add_widget(back_button)
        layout.add_widget(self.error_label)  # Добавляем метку в макет

        self.add_widget(layout)

    def register(self, instance):
        username = self.username.text
        password = sha256(self.password.text.encode()).hexdigest()
        secret_question = self.secret_question.text
        secret_answer = self.secret_answer.text

        # Подключение к базе данных и добавление пользователя
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, password, role, secret_question, secret_answer)
                VALUES (?, ?, 'user', ?, ?)
            """, (username, password, secret_question, secret_answer))
            conn.commit()
            self.manager.current = 'login'
        except sqlite3.IntegrityError:
            self.error_label.text = 'Пользователь уже существует!'  # Обновляем текст ошибки
        finally:
            conn.close()

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
