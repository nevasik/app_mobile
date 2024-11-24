import os
import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner  # Для выбора категории
from functools import partial

from database.database import get_db_path


class ViewAllRecipesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.recipes_label = Label(text='Список всех рецептов:')
        self.add_recipe_button = Button(text='Добавить рецепт', on_press=partial(self.change_screen, 'add_recipe'))
        self.delete_recipe_button = Button(text='Удалить рецепт', on_press=self.delete_recipe)
        back_btn = Button(text='Назад', on_press=partial(self.change_screen, 'admin_screen'))

        layout.add_widget(self.recipes_label)
        layout.add_widget(self.add_recipe_button)
        layout.add_widget(self.delete_recipe_button)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        """Вызывается при входе на экран, обновляет список рецептов."""
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.id, r.title, r.ingredients, r.instructions, c.name 
            FROM recipes r
            LEFT JOIN categories c ON r.category_id = c.id
        """)
        self.recipes = cursor.fetchall()
        conn.close()

        if self.recipes:
            recipes_text = "\n".join([
                f"{r[0]}. {r[1]} (Категория: {r[4] or 'Без категории'})\n"
                f"   Ингредиенты: {r[2]}\n"
                f"   Инструкция: {r[3]}"
                for r in self.recipes
            ])
        else:
            recipes_text = "Нет доступных рецептов."

        self.recipes_label.text = recipes_text

    def delete_recipe(self, instance):
        """Логика удаления первого рецепта из списка (для примера)."""
        if not self.recipes:
            self.recipes_label.text = "Нет доступных рецептов для удаления."
            return

        first_recipe_id = self.recipes[0][0]

        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipes WHERE id = ?", (first_recipe_id,))
        conn.commit()
        conn.close()

        self.on_enter()  # Обновление списка рецептов
        self.recipes_label.text = f"Рецепт с ID {first_recipe_id} успешно удален."

    def change_screen(self, screen_name, instance):
        """Переключение между экранами."""
        self.manager.current = screen_name


class AddRecipeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.title_input = TextInput(hint_text='Название рецепта')
        self.ingredients_input = TextInput(hint_text='Ингредиенты')
        self.instructions_input = TextInput(hint_text='Инструкция')
        self.category_spinner = Spinner(text='Выберите категорию', values=[])  # Заполнится в `on_pre_enter`
        save_button = Button(text='Сохранить рецепт', on_press=self.save_recipe)
        back_btn = Button(text='Назад', on_press=partial(self.change_screen, 'view_recipes'))

        layout.add_widget(Label(text='Добавление нового рецепта'))
        layout.add_widget(self.title_input)
        layout.add_widget(self.ingredients_input)
        layout.add_widget(self.instructions_input)
        layout.add_widget(self.category_spinner)
        layout.add_widget(save_button)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_pre_enter(self):
        """Заполнение списка категорий перед отображением экрана."""
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()
        conn.close()

        self.category_spinner.values = [f"{c[0]}: {c[1]}" for c in categories]
        self.category_spinner.text = 'Выберите категорию'  # Сбрасываем выбор

    def save_recipe(self, instance):
        """Сохранение нового рецепта в базу данных."""
        title = self.title_input.text.strip()
        ingredients = self.ingredients_input.text.strip()
        instructions = self.instructions_input.text.strip()
        category_text = self.category_spinner.text
        category_id = None

        if category_text != 'Выберите категорию':
            category_id = int(category_text.split(":")[0])

        if not title or not ingredients or not instructions:
            return  # Добавьте сообщение об ошибке, если хотите

        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO recipes (title, ingredients, instructions, category_id)
            VALUES (?, ?, ?, ?)
        """, (title, ingredients, instructions, category_id))

        conn.commit()
        conn.close()

        # Очистка полей ввода
        self.title_input.text = ''
        self.ingredients_input.text = ''
        self.instructions_input.text = ''
        self.category_spinner.text = 'Выберите категорию'

        self.change_screen('view_recipes', instance)

    def change_screen(self, screen_name, instance):
        """Переключение между экранами."""
        self.manager.current = screen_name
