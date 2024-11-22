from utils import *

from detail import DetailWindow
from home import HomeWindow
from login import LoginWindow
from showing import ShowingWindow
from history import HistoryWindow
from signup import SignupWindow

Window.maximize()
Builder.load_file('home.kv')
Builder.load_file('login.kv')
Builder.load_file('detail.kv')
Builder.load_file('showing.kv')
Builder.load_file('history.kv')
Builder.load_file('signup.kv')

print(Window.size)

class WindowManager(ScreenManager):
    pass

class GhibliApp(MDApp):
    def build(self):
        return super().build()

if __name__ == '__main__':
    GhibliApp().run()