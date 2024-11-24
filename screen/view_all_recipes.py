import sqlite3

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from functools import partial


class ViewAllRecipesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.recipes_label = Label(text='Список всех рецептов:')
        self.delete_recipes_button = Button(text='Удалить рецепт', on_press=self.delete_recipes)
        back_btn = Button(text='Назад', on_press=partial(self.change_screen, 'admin_screen'))

        layout.add_widget(self.recipes_label)
        layout.add_widget(self.delete_recipes_button)
        layout.add_widget(back_btn)

        self.add_widget(layout)

    def on_enter(self):
        conn = sqlite3.connect("../poplaukhin_db.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT t.id, u.username, t.type, t.amount, t.category, t.date 
            FROM recipes t
            JOIN users u ON t.user_id = u.id
        """)
        self.recipes = cursor.fetchall()
        conn.close()

        recipes_text = "\n".join(
            [f"{t[0]}. {t[1]} - {t[2]}: {t[3]:.2f} руб., {t[4]} ({t[5]})" for t in self.recipes])
        self.recipes_label.text = recipes_text if self.recipes else "Нет рецепта"

    def delete_recipes(self, instance):
        if not self.recipes:
            return

        self.delete_recipes_button.text = "Вы уверены, что хотите удалить этот рецепт?"
        self.delete_recipes_button.on_press = self.confirm_recipes_button

    def confirm_recipes_button(self, instance):
        id_recipes = self.recipes[0]
        conn = sqlite3.connect("../poplaukhin_db.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM recipes WHERE id=?", (id_recipes[0],))
        conn.commit()
        conn.close()

        self.on_enter()  # Обновляем список транзакций после удаления
        self.delete_recipes_button.text = "Удалить рецепт"
        self.delete_recipes_button.on_press = self.delete_recipes  # Сбрасываем кнопку

    def change_screen(self, screen_name, instance):
        self.manager.current = screen_name
