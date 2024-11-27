import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.anchorlayout import AnchorLayout
from hashlib import sha256
from functools import partial

from database.database import get_db_path


class PasswordRecoveryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Основной макет с фоном
        layout = FloatLayout()

        # Фоновое изображение
        background = Image(
            source='/Users/mac/PycharmProjects/app_poplaukhin/static/grey.jpg',
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )
        layout.add_widget(background)

        # Центральный макет для элементов (уменьшенный размер)
        center_layout = AnchorLayout(
            anchor_x='center',
            anchor_y='center'
        )
        box_layout = BoxLayout(
            orientation='vertical',
            spacing=15,
            padding=[20, 20],
            size_hint=(0.6, 0.6)  # Уменьшение размера
        )

        # Заголовок
        title_label = Label(
            text='[b]Восстановление пароля[/b]',
            markup=True,
            font_size=24,
            color=(1, 1, 1, 1)
        )
        box_layout.add_widget(title_label)

        # Поля ввода
        self.username = TextInput(
            hint_text='Имя пользователя',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.secret_question = Label(
            text='Секретный вопрос:',
            font_size=30,
            color=(1, 1, 1, 1)
        )
        self.secret_answer = TextInput(
            hint_text='Ответ на секретный вопрос',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.new_password = TextInput(
            hint_text='Новый пароль',
            multiline=False,
            password=True,
            size_hint_y=None,
            height=50
        )

        box_layout.add_widget(self.username)
        box_layout.add_widget(self.secret_question)
        box_layout.add_widget(self.secret_answer)
        box_layout.add_widget(self.new_password)

        # Кнопки
        recovery_button = Button(
            text='Восстановить пароль',
            size_hint_y=None,
            height=50,
            background_color=(0.3, 0.6, 0.9, 1),
            color=(1, 1, 1, 1),
            on_press=self.recover_password
        )
        back_button = Button(
            text='Назад',
            size_hint_y=None,
            height=50,
            background_color=(0.9, 0.4, 0.4, 1),
            color=(1, 1, 1, 1),
            on_press=partial(self.change_screen, 'login')
        )
        box_layout.add_widget(recovery_button)
        box_layout.add_widget(back_button)

        # Добавляем в центральный макет
        center_layout.add_widget(box_layout)
        layout.add_widget(center_layout)

        self.add_widget(layout)

    def recover_password(self, instance):
        """Восстановление пароля."""
        username = self.username.text
        answer = self.secret_answer.text
        if username == 'admin':  # если это admin, то вставляем обычный пароль, так как в бд вставлен дефолтный пароль admin
            new_password = self.new_password.text
        else:
            new_password = sha256(self.new_password.text.encode()).hexdigest()

        path = get_db_path()
        conn = sqlite3.connect(path)
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
            error_label = Label(
                text='Неверный ответ на секретный вопрос!',
                color=(1, 0, 0, 1)
            )
            self.add_widget(error_label)
        conn.close()

    def change_screen(self, screen_name, instance):
        """Переключение между экранами."""
        self.manager.current = screen_name
