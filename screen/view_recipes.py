import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial

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
        conn = sqlite3.connect("../poplaukhin_db.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT type, amount, category, date 
            FROM recipes 
            WHERE user_id = ?
        """, (1,))  # Здесь 1 замените на текущего пользователя
        recipes = cursor.fetchall()
        conn.close()

        recipes_text = "\n".join([f"{t[0]}: {t[1]:.2f} руб., {t[2]} ({t[3]})" for t in recipes])
        self.recipes_label.text = recipes_text if recipes else "Нет рецептов"

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name