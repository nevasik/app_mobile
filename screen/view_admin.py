from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial


class AdminScreen_view(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        view_users_btn = Button(text='Просмотреть пользователей', on_press=partial(self.change_screen, 'view_users'))
        view_all_recipes_btn = Button(text='Просмотреть все рецепты', on_press=partial(self.change_screen, 'view_all_recipes'))
        back_btn = Button(text='Выйти', on_press=partial(self.change_screen, 'login'))

        layout.add_widget(Label(text='Администратор'))
        layout.add_widget(view_users_btn)
        layout.add_widget(view_all_recipes_btn)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
