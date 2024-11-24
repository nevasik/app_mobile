from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screen.view_admin import AdminScreen_view
from database.database import init_db
from screen.view_password import PasswordRecoveryScreen
from screen.view_login import LoginScreen
from screen.view_registration import RegistrationScreen
from core.user import UserScreen
from screen.view_all_recipes import ViewAllRecipesScreen
from screen.view_recipes import ViewRecipesScreen
from screen.view_user import ViewUsersScreen

class Recipes(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(PasswordRecoveryScreen(name='password_recovery'))
        sm.add_widget(UserScreen(name='user_screen'))
        sm.add_widget(AdminScreen_view(name='admin_screen'))
        sm.add_widget(ViewUsersScreen(name='view_users'))
        sm.add_widget(ViewAllRecipesScreen(name='view_all_recipes'))
        sm.add_widget(ViewRecipesScreen(name='view_recipes'))
        return sm


if __name__ == "__main__":
    init_db()
    Recipes().run()
