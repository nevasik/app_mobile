import sqlite3

from decorator import append
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from functools import partial
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from database.database import get_db_path


class ViewRecipesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Лейаут для экрана
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.background = Image(
            source='/Users/mac/PycharmProjects/app_poplaukhin/static/black_background.png',
            allow_stretch=True,
            keep_ratio=False,
        )
        layout.add_widget(self.background)

        # Добавим Label для отображения всех рецептов
        self.recipe_list_label = Label(
            text="Рецепты:",  # Этот текст можно будет обновлять динамически
            size_hint=(None, None),
            size=(300, 50),
            color=(1, 0, 1, 1),
            pos_hint={'center_x': 0.5, 'top': 0.3},  # Расположим Label чуть ниже кнопки "Добавить рецепт"
        )
        layout.add_widget(self.recipe_list_label)

        # Создадим BoxLayout для списка рецептов
        self.recipe_list_layout = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            size=(300, 300),  # Ограничим высоту списка
            pos_hint={'center_x': 0.5, 'top': 0.2},  # Расположим список ниже Label
        )
        layout.add_widget(self.recipe_list_layout)

        # Заполним список рецептов
        self.load_recipes()

        self.recipe_id_input = TextInput(
            hint_text="Введите ID рецепта",
            size_hint=(None, None),  # Убираем size_hint для ширины и высоты, чтобы вручную задать размер
            size=(300, 50),  # Устанавливаем размеры
            pos_hint={'center_x': 0.5, 'top': 1},  # Размещаем в верхней части экрана, центрируем по горизонтали
        )
        layout.add_widget(self.recipe_id_input)

        # Кнопка для просмотра рецепта
        view_button = Button(
            text="Посмотреть рецепт",
            background_color=(1, 1, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.4},
        )
        view_button.bind(on_press=self.show_recipe_by_id)
        layout.add_widget(view_button)

        # Кнопка для редактирования рецепта
        edit_button = Button(
            text="Редактировать рецепт",
            background_color=(0, 1, 0, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.4},
        )

        edit_button.bind(on_press=self.edit_recipe)
        layout.add_widget(edit_button)

        # back_btn = Button(text='Назад', on_press=partial(self.change_screen, 'admin_screen'))
        # Кнопка: Выйти
        back_btn = Button(
            text='Выйти',
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'top': 0.4},
            on_press=partial(self.change_screen, 'admin_screen'),
        )
        layout.add_widget(back_btn)

        # Добавляем лейаут на экран
        self.add_widget(layout)

    def load_recipes(self):
        # Подключаемся к базе данных
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем все рецепты
        cursor.execute("""
            SELECT id, title FROM recipes
        """)
        recipes = cursor.fetchall()
        conn.close()

        # Формируем строку с id и title рецептов
        recipes_text = ""
        for recipe in recipes:
            recipes_text += f"ID: {recipe[0]} - {recipe[1]}\n"

        # Обновляем текст в label с рецептами
        self.recipe_list_label.text = f"Рецепты:\n{recipes_text}"

    def change_screen(self, screen_name, instance):
        self.load_recipes()
        self.manager.current = screen_name

    def show_recipe_by_id(self, instance):
        self.load_recipes()
        recipe_id = self.recipe_id_input.text.strip()

        if not recipe_id:
            self.show_popup("Ошибка", "Пожалуйста, введите ID рецепта")
            return

        try:
            recipe_id = int(recipe_id)
        except ValueError:
            self.show_popup("Ошибка", "ID должен быть числовым значением")
            return

        # Подключаемся к базе данных
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем рецепт по ID
        cursor.execute("""
            SELECT title, ingredients, instructions
            FROM recipes
            WHERE id = ?
        """, (recipe_id,))
        recipe = cursor.fetchone()
        conn.close()

        if recipe:
            recipe_text = (
                f"Название: {recipe[0]}\n\n"
                f"Ингредиенты: {recipe[1]}\n\n"
                f"Инструкция: {recipe[2]}\n"
            )
            self.show_popup("Рецепт", recipe_text)
        else:
            self.show_popup("Ошибка", "Рецепт не найден")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

    def edit_recipe(self, instance):
        recipe_id = self.recipe_id_input.text.strip()

        if not recipe_id:
            self.show_popup("Ошибка", "Пожалуйста, введите ID рецепта для редактирования")
            return

        try:
            recipe_id = int(recipe_id)
        except ValueError:
            self.show_popup("Ошибка", "ID должен быть числовым значением")
            return

        # Подключаемся к базе данных
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем рецепт по ID для редактирования
        cursor.execute("""
            SELECT title, ingredients, instructions
            FROM recipes
            WHERE id = ?
        """, (recipe_id,))
        recipe = cursor.fetchone()
        conn.close()

        if recipe:
            self.manager.current = 'edit_recipe'
            self.manager.get_screen('edit_recipe').load_recipe(recipe_id, recipe)
        else:
            self.show_popup("Ошибка", "Рецепт не найден")


class AddRecipeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Заголовок
        title_label = Label(
            text="Добавить рецепт",
            font_size=40,
            color=(1, 0.5, 0, 1),  # Оранжевый цвет для заголовка
            size_hint=(None, None),
            size=(1000, 150),  # Увеличен размер области заголовка
            pos_hint={'center_x': 0.5, 'top': 0.9},
        )
        layout.add_widget(title_label)

        # Название рецепта
        title_input = TextInput(
            hint_text='Название рецепта',
            font_size=40,
            size_hint=(None, None),
            size=(1000, 150),  # Увеличен размер области заголовка
            pos_hint={'center_x': 0.5, 'top': 0.75},
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1),  # Светло-серый фон для текстового поля
            foreground_color=(0, 0, 0, 1),  # Черный цвет текста
            border=(10, 10, 10, 10),  # Скругленные углы
            padding=(10, 10),  # Отступы внутри поля
        )
        layout.add_widget(title_input)

        # Ингредиенты
        ingredients_input = TextInput(
            hint_text='Ингредиенты',
            font_size=40,
            size_hint=(None, None),
            size=(1000, 150),  # Увеличен размер области заголовка
            pos_hint={'center_x': 0.5, 'top': 0.6},
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
            border=(10, 10, 10, 10),
            padding=(10, 10),
            multiline=True,
        )
        layout.add_widget(ingredients_input)

        # Инструкция
        instructions_input = TextInput(
            hint_text='Инструкция',
            font_size=40,
            size_hint=(None, None),
            size=(1000, 150),  # Увеличен размер области заголовка
            pos_hint={'center_x': 0.5, 'top': 0.45},
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1),
            border=(10, 10, 10, 10),
            padding=(10, 10),
            multiline=True,
        )
        layout.add_widget(instructions_input)

        self.category_spinner = Spinner(  # Заполнится в `on_pre_enter`
            text='Выберите категорию',
            values=[],
            font_size=40,
            size_hint=(None, None),
            size=(1000, 150),  # Увеличен размер области заголовка
            pos_hint={'center_x': 0.5, 'top': 0.3},
            background_color=(0.9, 0.9, 0.9, 1),
            background_normal='',
            color=(0, 0, 0, 1),
        )
        layout.add_widget(self.category_spinner)

        # Кнопка "Сохранить рецепт"
        save_button = Button(
            text='Сохранить рецепт',
            on_press=self.save_recipe,
            background_color=(0.2, 0.7, 0.3, 1),  # Зеленый цвет кнопки
            color=(1, 1, 1, 1),  # Белый цвет текста на кнопке
            font_size=40,
            size_hint=(None, None),
            size=(700, 150),  # Увеличен размер области заголовка
            pos_hint={'center_x': 0.5, 'top': 0.15},
            border=(5, 5, 5, 5),
        )
        layout.add_widget(save_button)

        # Кнопка "Назад"
        back_btn = Button(
            text='Назад',
            on_press=partial(self.change_screen, 'view_recipes'),
            background_color=(0.8, 0.2, 0.2, 1),  # Красный цвет для кнопки
            color=(1, 1, 1, 1),
            font_size=40,
            size_hint=(None, None),
            size=(700, 150),  # Увеличен размер области заголовка
            pos_hint={'center_x': 0.5, 'top': 0.05},
            border=(5, 5, 5, 5),
        )
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

        self.change_screen('admin_screen', instance)

    def change_screen(self, screen_name, instance):
        """Переключение между экранами."""
        self.manager.current = screen_name


class EditRecipeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.title_input = TextInput(
            hint_text="Название рецепта",
            size_hint=(None, None),  # Убираем size_hint для ширины и высоты, чтобы вручную задать размер
            size=(300, 50),  # Устанавливаем размеры
            pos_hint={'center_x': 0.5, 'top': 1},  # Размещаем в верхней части экрана, центрируем по горизонтали
        )
        layout.add_widget(self.title_input)

        # Поле для ingredients
        self.ingredients_input = TextInput(
            hint_text="Ингредиенты",
            size_hint=(None, None),  # Убираем size_hint для ширины и высоты, чтобы вручную задать размер
            size=(300, 50),  # Устанавливаем размеры
            pos_hint={'center_x': 0.5, 'top': 1},  # Размещаем в верхней части экрана, центрируем по горизонтали
        )
        layout.add_widget(self.ingredients_input)

        # Поле для instructions
        self.instructions_input = TextInput(
            hint_text="Инструкция",
            size_hint=(None, None),  # Убираем size_hint для ширины и высоты, чтобы вручную задать размер
            size=(300, 50),  # Устанавливаем размеры
            pos_hint={'center_x': 0.5, 'top': 1},  # Размещаем в верхней части экрана, центрируем по горизонтали
        )
        layout.add_widget(self.instructions_input)

        # Кнопка для сохранения изменений
        save_button = Button(
            text="Сохранить изменения",
            size_hint=(None, None),  # Убираем size_hint для ширины и высоты, чтобы вручную задать размер
            size=(300, 50),  # Устанавливаем размеры
            pos_hint={'center_x': 0.5, 'top': 1},  # Размещаем в верхней части экрана, центрируем по горизонтали
        )
        save_button.bind(on_press=self.save_recipe)
        layout.add_widget(save_button)

        # Добавляем лейаут на экран
        self.add_widget(layout)

    def load_recipe(self, recipe_id, recipe_data):
        self.recipe_id = recipe_id
        self.title_input.text = recipe_data[0]
        self.ingredients_input.text = recipe_data[1]
        self.instructions_input.text = recipe_data[2]

    def save_recipe(self, instance):
        title = self.title_input.text.strip()
        ingredients = self.ingredients_input.text.strip()
        instructions = self.instructions_input.text.strip()

        if not title or not ingredients or not instructions:
            self.show_popup("Ошибка", "Все поля должны быть заполнены")
            return

        # Подключаемся к базе данных и обновляем рецепт
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE recipes
            SET title = ?, ingredients = ?, instructions = ?
            WHERE id = ?
        """, (title, ingredients, instructions, self.recipe_id))
        conn.commit()
        conn.close()

        self.change_screen('view_recipes', instance)
        self.show_popup("Успех", "Рецепт успешно обновлен")

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(0.6, 0.4))
        popup.open()

    def change_screen(self, screen_name, instance):
        """Переключение между экранами."""
        self.manager.current = screen_name
