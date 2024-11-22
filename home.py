from utils import *


class Home(BoxLayout):
    # Enjoy with Ghibli
    joy_label = CoreLabel(text="Enjoy with\nGhibli", font_size=dp(100), font_name="assets/fonts/ArchitectsDaughter-Regular.ttf")
    joy_label.refresh() # Refresh mới tải lên được
    joy_label = joy_label.texture

    # Các hằng và biến
    IMAGE_BACKGROUND_PATH = 'assets/images/background/' # Đường dẫn vào ảnh nền
    IMG_NUM = len(os.listdir(IMAGE_BACKGROUND_PATH)) - 2 # Số lượng ảnh nền của Home
    image_index = 1 # Chỉ số ảnh nền
    image_path = StringProperty(f"{IMAGE_BACKGROUND_PATH}bg1.jpg") # Đường dẫn ảnh nền

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_background, 3.0) # Lên lịch thay đổi nền liên tục
    
    # Cập nhật nền
    def update_background(self, dt):
        self.image_index += 1 # Tăng chỉ số nền
        if self.image_index > self.IMG_NUM:
            self.image_index = 1
        self.image_path = f"{self.IMAGE_BACKGROUND_PATH}bg{self.image_index}.jpg"


class HomeWindow(Screen):
    def sign_out(self):
        sign_in_button = self.ids.sign_in_button
        sign_in_button.text, sign_in_button.opacity, sign_in_button.disabled,sign_in_button.size_hint = "Đăng nhập", 1, False, (.5, 1)
        
        login_page = self.parent.ids.login_page
        login_page.access_token, login_page.user = None, None

        history_page = self.parent.ids.history_page

        history_button = self.ids.history_button
        history_button.disabled = True