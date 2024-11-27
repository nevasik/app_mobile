from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from functools import partial

class UserDefaultScreenView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        self.background = Image(
            source='/Users/mac/PycharmProjects/app_poplaukhin/static/background.jpg',
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(self.background)

        # Заголовок
        title = Label(
            text='Пользователь',
            font_size=32,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'top': 0.95},
        )
        layout.add_widget(title)

        # Кнопка: Просмотреть все рецепты
        view_all_recipes_btn = Button(
            text='Просмотреть все рецепты',
            background_color=(0.4, 0.10, 0.6, 2),
            color=(1, 1, 1, 1),
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.55},
            on_press=partial(self.change_screen, 'view_recipes'),
        )
        layout.add_widget(view_all_recipes_btn)

        # Кнопка: Выйти
        back_btn = Button(
            text='Выйти',
            background_color=(0.10, 0.12, 0.10, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            on_press=partial(self.change_screen, 'login'),
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
