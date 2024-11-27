import sqlite3
from functools import partial
from hashlib import sha256

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from database.database import get_db_path


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Фоновое изображение
        self.background = Image(
            source='/Users/mac/PycharmProjects/app_poplaukhin/static/background.jpg',
            allow_stretch=True,
            keep_ratio=False
        )
        self.add_widget(self.background)

        # Основной слой
        layout = RelativeLayout()

        # Вложенный слой с виджетами
        form_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.8, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # Текстовые поля
        self.username = TextInput(
            hint_text='Имя пользователя',
            multiline=False,
            size_hint=(1, 0.15),
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
        )

        self.password = TextInput(
            hint_text='Пароль',
            multiline=False,
            password=True,
            size_hint=(1, 0.15),
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
        )

        # Кнопки
        login_button = Button(
            text='Войти',
            size_hint=(1, 0.15),
            background_color=(0, 0.5, 0.7, 1),
            color=(1, 1, 1, 1),
            on_press=self.login,
        )
        
        register_button = Button(
            text='Создать аккаунт',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            on_press=partial(self.change_screen, 'registration'),
        )

        reset_password_button = Button(
            text='Восстановить пароль',
            size_hint=(1, 0.15),
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            on_press=partial(self.change_screen, 'password_recovery'),
        )

        # Добавление виджетов
        form_layout.add_widget(Label(
            text='Авторизация',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.8},
            color=(0, 0, 0, 1))
        )
        
        form_layout.add_widget(self.username)
        form_layout.add_widget(self.password)
        form_layout.add_widget(login_button)
        form_layout.add_widget(register_button)
        form_layout.add_widget(reset_password_button)

        layout.add_widget(form_layout)
        self.add_widget(layout)

    def login(self, instance):
        username = self.username.text
        if username == 'admin':
            hashed_password = self.password.text
        else:
            hashed_password = sha256(self.password.text.encode()).hexdigest()

        # Подключение к базе данных
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        conn.close()

        if user:
            if user[0] == 'admin':
                self.manager.current = 'admin_screen'
            else:
                self.manager.current = 'user_default_screen'
        else:
            self.username.text = ''
            self.password.text = ''
            self.add_widget(Label(text='Неверные данные!', size_hint=(1, 0.1), color=(1, 0, 0, 1)))

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
