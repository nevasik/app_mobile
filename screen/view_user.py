import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from functools import partial
from database.database import get_db_path


class ViewUsersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        # Задний фон
        self.background = Image(
            source='/Users/mac/PycharmProjects/app_poplaukhin/static/black.jpg',
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(self.background)

        # Заголовок
        self.users_label = Label(
            text='Список пользователей:',
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(300, 50),
            pos_hint={'center_x': 0.5, 'top': 0.9},
        )
        layout.add_widget(self.users_label)

        # Поле ввода для ID
        self.user_id_input = TextInput(
            hint_text='Введите ID пользователя',
            multiline=False,
            size_hint=(0.4, 0.07),
            pos_hint={'center_x': 0.5, 'top': 0.75},
            background_color=(0.2, 0.2, 0.2, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
        )
        layout.add_widget(self.user_id_input)

        # Кнопка назначения администратором
        self.make_admin_button = Button(
            text='Сделать администратором',
            background_color=(0, 0.6, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.65},
            on_press=self.make_admin,
        )
        layout.add_widget(self.make_admin_button)

        # Кнопка удаления пользователя
        self.delete_user_button = Button(
            text='Удалить пользователя',
            background_color=(0.7, 0, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.55},
            on_press=self.delete_user,
        )
        layout.add_widget(self.delete_user_button)

        # Кнопка назад
        back_btn = Button(
            text='Назад',
            background_color=(0.2, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.45},
            on_press=partial(self.change_screen, 'admin_screen'),
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        # Подключение к базе данных и загрузка пользователей
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        self.users = cursor.fetchall()
        conn.close()

        # Обновление текста со списком пользователей
        users_text = "\n".join([f"{u[0]}. {u[1]} ({u[2]})" for u in self.users])
        self.users_label.text = users_text if self.users else "Нет зарегистрированных пользователей"

    def make_admin(self, instance):
        user_id = self.user_id_input.text.strip()

        if not user_id.isdigit():
            self.users_label.text = "Введите корректный ID пользователя"
            return

        # Обновление роли пользователя
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = 'admin' WHERE id = ?", (user_id,))
        conn.commit()
        updated_rows = cursor.rowcount
        conn.close()

        if updated_rows > 0:
            self.users_label.text = f"Пользователь с ID {user_id} стал администратором"
            self.on_enter()  # Обновление списка пользователей
        else:
            self.users_label.text = f"Пользователь с ID {user_id} не найден"

    def delete_user(self, instance):
        if self.delete_user_button.text == "Вы уверены?":
            # Если текст уже изменен, вызовем подтверждение
            self.confirm_delete(instance)
        else:
            # Изменяем текст кнопки и устанавливаем текущий обработчик
            self.delete_user_button.text = "Вы уверены?"
            self.delete_user_button.on_press = partial(self.confirm_delete, instance)

    def confirm_delete(self, instance):
        user_id = self.user_id_input.text.strip()

        if not user_id.isdigit():
            self.users_label.text = "Введите корректный ID пользователя"
            return

        # Удаление пользователя
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        deleted_rows = cursor.rowcount
        conn.close()

        if deleted_rows > 0:
            self.users_label.text = f"Пользователь с ID {user_id} удален"
        else:
            self.users_label.text = f"Пользователь с ID {user_id} не найден"

        # Обновление списка пользователей
        self.on_enter()

        # Сброс кнопки
        self.delete_user_button.text = "Удалить пользователя"
        self.delete_user_button.on_press = self.delete_user

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
