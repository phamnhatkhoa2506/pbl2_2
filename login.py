from utils import *

class LoginWindow(Screen):
    access_token = None # token
    user = None 

    # Các thuộc tính
    NOTIFI_SUCCESS_COLOR = (0, 1, 0)

    def get_input(self):
        self.username = self.ids.username # Lấy tên đăng nhập
        self.password = self.ids.password # Lấy mật khẩu
        self.login_notification = self.ids.login_status # lấy label thông báo tình trang đăng nhập

        # Kiểm tra xem có để trống thông tin không
        if self.username.text == "":
            if self.password.text == "": 
                self.login_notification.text = "Không thể để trống thông tin"
            else: 
                self.login_notification.text = "Không thể để trống tên đăng nhập"
            return
        elif self.password.text == "":
            self.login_notification.text = "Không thể để trống mật khẩu"
            return

        # Gọi API đăng nhập
        login_res = login({'username' : self.username.text, 'password': self.password.text})

        # Đưa thông tin gọi API
        if login_res[0] == 400: # Sai thông tin
            self.login_notification.text = login_res[1]
        else: # Đăng nhập thành công
            # Thanh thông báo khi thành công
            self.login_notification.text = "Đăng nhập thành công"
            self.login_notification.color = self.NOTIFI_SUCCESS_COLOR
    
            # Ẩn nút đăng nhập ở Home
            sign_in_button = self.parent.ids.home_page.ids.sign_in_button
            sign_in_button.text, sign_in_button.opacity, sign_in_button.disabled,sign_in_button.size_hint = "", 0, True, (0, 0)

            history_button = self.parent.ids.home_page.ids.history_button
            history_button.disabled = False
            
            self.access_token = login_res[1]['token'] # Lưu trữ token
            self.user = self.username

            history_page = self.parent.ids.history_page
            history_page.update(self.access_token)
            history = history_page.ids.history
            history.update()

            self.go_back() # Quay trở trang home

    def go_back(self, *args):
        # Trì hoãn chuyển trang
        Clock.schedule_once(self.change_screen, .5)

    def change_screen(self, dt):
        # Reset lại login form khi đăng nhập thành công
        self.manager.current = 'home'
        self.manager.transition.direction = "up"
        self.login_notification.text = ""
        self.username.text = ""
        self.password.text = ""

    def to_sign_up_page(self):
        self.manager.current = 'signup'
        self.manager.transition.direction = "down"