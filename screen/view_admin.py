from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from functools import partial

class AdminScreenView(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = FloatLayout()

        self.background = Image(
            source='/Users/mac/PycharmProjects/app_poplaukhin/static/black_background.png',
            allow_stretch=True,
            keep_ratio=False,
        )

        layout.add_widget(self.background)

        # Заголовок
        title = Label(
            text='Администратор',
            font_size=32,
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'top': 0.95},
        )
        layout.add_widget(title)

        # Кнопка: Просмотреть пользователей
        view_users_btn = Button(
            text='Просмотреть пользователей',
            background_color=(0, 0.5, 0.7, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.7},
            on_press=partial(self.change_screen, 'view_user'),
        )
        layout.add_widget(view_users_btn)

        # Кнопка: Просмотреть все рецепты
        view_all_recipes_btn = Button(
            text='Просмотреть все рецепты',
            background_color=(0.2, 0.6, 0.3, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.55},
            on_press=partial(self.change_screen, 'view_recipes'),
        )
        layout.add_widget(view_all_recipes_btn)

        # Кнопка: Добавить рецепт
        add_recipe_btn = Button(
            text='Добавить рецепт',
            background_color=(0.7, 0.7, 0.3, 1),  # Желтый цвет для кнопки
            color=(1, 1, 1, 1),
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            on_press=partial(self.change_screen, 'add_recipe'),  # Переход на экран добавления рецепта
        )
        layout.add_widget(add_recipe_btn)

        # Кнопка: Выйти
        back_btn = Button(
            text='Выйти',
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.25},
            on_press=partial(self.change_screen, 'login'),
        )
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
