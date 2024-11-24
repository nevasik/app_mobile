import os
import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial

from database.database import get_db_path


class ViewUsersScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.users_label = Label(text='Список пользователей:')
        self.delete_user_button = Button(text='Удалить пользователя', on_press=self.delete_user)
        back_btn = Button(text='Назад', on_press=partial(self.change_screen, 'admin_screen'))

        layout.add_widget(self.users_label)
        layout.add_widget(self.delete_user_button)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        # Подключение к базе данных и добавление рецепта
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        self.users = cursor.fetchall()
        conn.close()

        users_text = "\n".join([f"{u[0]}. {u[1]} ({u[2]})" for u in self.users])
        self.users_label.text = users_text if self.users else "Нет зарегистрированных пользователей"

    def delete_user(self, instance):
        if not self.users:
            return

        # Вопрос о подтверждении удаления
        self.delete_user_button.text = "Вы уверены, что хотите удалить этого пользователя?"
        self.delete_user_button.on_press = self.confirm_delete

    def confirm_delete(self, instance):
        user_to_delete = self.users[0]  # Для примера выбираем первого пользователя (потом можно будет улучшить)
        # Подключение к базе данных и добавление рецепта
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id=?", (user_to_delete[0],))
        conn.commit()
        conn.close()

        self.on_enter()  # Обновляем список пользователей после удаления
        self.delete_user_button.text = "Удалить пользователя"
        self.delete_user_button.on_press = self.delete_user  # Сбрасываем кнопку

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name