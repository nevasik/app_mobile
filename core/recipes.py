import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from functools import partial

from database.database import get_db_path


class RecipesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Поля ввода для добавления рецепта
        self.title = TextInput(hint_text='Название рецепта', multiline=False)
        self.ingredients = TextInput(hint_text='Ингредиенты (через запятую)', multiline=False)
        self.instructions = TextInput(hint_text='Инструкции', multiline=True)
        self.category = TextInput(hint_text='Категория', multiline=False)

        # Кнопки
        add_button = Button(text='Добавить рецепт', on_press=self.add_recipe)
        back_button = Button(text='Назад', on_press=partial(self.change_screen, 'user_screen'))

        # Добавление виджетов в макет
        layout.add_widget(Label(text='Добавление нового рецепта'))
        layout.add_widget(self.title)
        layout.add_widget(self.ingredients)
        layout.add_widget(self.instructions)
        layout.add_widget(self.category)
        layout.add_widget(add_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def add_recipe(self, instance):
        title = self.title.text
        ingredients = self.ingredients.text
        instructions = self.instructions.text
        category = self.category.text

        if not title or not ingredients or not instructions or not category:
            print("Пожалуйста, заполните все поля.")
            return

        # Подключение к базе данных и добавление рецепта
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO recipes (title, ingredients, instructions, category_id)
            VALUES (?, ?, ?, (
                SELECT id FROM categories WHERE name = ? LIMIT 1
            ))
        """, (title, ingredients, instructions, category))
        conn.commit()
        conn.close()

        print(f"Рецепт '{title}' успешно добавлен!")
        # Очистка полей после добавления
        self.title.text = ''
        self.ingredients.text = ''
        self.instructions.text = ''
        self.category.text = ''

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name