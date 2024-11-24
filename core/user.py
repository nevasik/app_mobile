import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial

class UserScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.greeting = Label(text='Добро пожаловать, пользователь!')
        add_recipes_btn = Button(text='Добавить рецепт', on_press=partial(self.change_screen, 'add_recipes'))
        view_recipes_btn = Button(text='Просмотреть рецепт', on_press=partial(self.change_screen, 'view_recipes'))
        back_btn = Button(text='Выйти', on_press=partial(self.change_screen, 'login'))

        layout.add_widget(self.greeting)
        layout.add_widget(add_recipes_btn)
        layout.add_widget(view_recipes_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
