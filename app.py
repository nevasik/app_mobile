from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screen.view_admin import AdminScreenView
from database.database import init_db
from screen.view_default_user import UserDefaultScreenView
from screen.view_reset_password import PasswordRecoveryScreen
from screen.view_login import LoginScreen
from screen.view_registration import RegistrationScreen
from screen.view_recipes import ViewRecipesScreen, AddRecipeScreen, EditRecipeScreen
from screen.view_user import ViewUsersScreen

class Recipes(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(PasswordRecoveryScreen(name='password_recovery'))
        sm.add_widget(AdminScreenView(name='admin_screen'))
        sm.add_widget(UserDefaultScreenView(name='user_default_screen'))
        sm.add_widget(ViewRecipesScreen(name='view_recipes'))
        sm.add_widget(ViewUsersScreen(name='view_user'))
        sm.add_widget(AddRecipeScreen(name='add_recipe'))
        sm.add_widget(EditRecipeScreen(name='edit_recipe'))

        return sm


if __name__ == "__main__":
    init_db()
    Recipes().run()
