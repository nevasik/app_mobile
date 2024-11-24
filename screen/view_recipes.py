import sqlite3
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial

from database.database import get_db_path


class ViewRecipesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.recipes_label = Label(text='Список рецептов:')
        back_btn = Button(text='Назад', on_press=partial(self.change_screen, 'user_screen'))

        layout.add_widget(self.recipes_label)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        """Вызывается при входе на экран, обновляет список рецептов."""
        path = get_db_path()
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT r.title, r.ingredients, r.instructions, c.name 
            FROM recipes r
            LEFT JOIN categories c ON r.category_id = c.id
        """)  # Здесь 1 замените на текущего пользователя
        recipes = cursor.fetchall()
        conn.close()

        # Формирование текста для отображения рецептов
        if recipes:
            recipes_text = "\n".join([
                f"{r[0]} (Категория: {r[3] if r[3] else 'Без категории'})\n"
                f"   Ингредиенты: {r[1]}\n"
                f"   Инструкция: {r[2]}"
                for r in recipes
            ])
        else:
            recipes_text = "Нет доступных рецептов."

        self.recipes_label.text = recipes_text

    def change_screen(self, screen_name, instance):
        """Переключение между экранами."""
        self.manager.current = screen_name