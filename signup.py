from utils import *
import re
from datetime import datetime

class SignupWindow(Screen):
    information = {}

    # Các thuộc tính
    NOTIFI_SUCCESS_COLOR = (0, 1, 0)

    @staticmethod
    def _validate_name(name: str):
        pattern = r'^[a-zA-Z ]+$'  
        if re.match(pattern, name):
            return True
        else:
            return False
        
    @staticmethod
    def _validate_account(name: str):
        pattern = r'^[A-Za-z0-9]+$'  
        if re.match(pattern, name):
            return True
        else:
            return False

    @staticmethod
    def _validate_password(s):
        return bool(re.match(r'^\S+$', s)) 

    @staticmethod
    def _validate_email(email):
        pattern = r'^[a-zA-Z0-9]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def _validate_date(date_str):
        try:
            # Try parsing with format DD/MM/YYYY
            datetime.strptime(date_str, '%d/%m/%Y')
            return True
        except ValueError:
            # If there's a ValueError, the date is not valid
            return False

    def _check_information(self, information: dict):
        if information['firstname'] == "":
            return (False, "Không được để trống họ và tên đệm")
        if information['lastname'] == "":
            return (False, "Không được để trống tên")
        if information['username'] == "":
            return (False, "Không được để trống tên đăng nhập")
        if information['password'] == "":
            return (False, "Không được để trống mật khẩu")
        if information['email'] == "":
            return (False, "Không được để trống email")
        if information['birthday'] == "":
            return (False, "Không được để trống ngày sinh")

        if not self._validate_name(information['firstname']):
            return (False, "Họ và têm đệm không hợp lệ (kí tự hợp lệ: A-Z, a-z)")
        if not self._validate_name(information['lastname']):
            return (False, "Tên không hợp lệ (kí tự hợp lệ: A-Z, a-z, viết hoa đầu từ)")
        if not self._validate_account(information['username']):
            return (False, "Tên đăng nhập không hợp lệ (kí tự hợp lệ: A-Z, a-z, 0-9)")
        if not self._validate_account(information['password']):
            return (False, "Mật khẩu không hợp lệ (không chứa khoảng trắng)")
        if not self._validate_email(information['email']):
            return (False, "Email không hợp lệ")
        if not self._validate_date(information['birthday']):
            return (False, "Ngày sinh không hợp lệ")

        return (True, "Đăng ký thành công")

    def get_input(self):
        print("SignUp Information:")
        self.information['firstname'] = self.ids.firstname.text
        print(f"\tFirst Name: {self.information['firstname']}")
        self.information['lastname'] = self.ids.lastname.text
        print(f"\tLast Name: {self.information['lastname']}")
        self.information['username'] = self.ids.username.text # Lấy tên đăng nhập
        print(f"\tUser Name: {self.information['username']}")
        self.information['password'] = self.ids.password.text # Lấy mật khẩu
        print(f"\tPassword: {self.information['password']}")
        self.information['email'] = self.ids.email.text
        print(f"\tEmail: {self.information['email']}")
        self.information['birthday'] = self.ids.birthday.text
        print(f"\tBirthday: {self.information['birthday']}")
        self.signup_notification = self.ids.signup_status # lấy label thông báo tình trang đăng nhập
        print(f"Notification: {self.signup_notification.text}")

        check: tuple[bool, str] = self._check_information(self.information)
        if not check[0]:
            self.signup_notification.text = check[1]
            print(f"SignUp Error: {self.signup_notification.text}")
            return
        
        self.information['birthday'] = "-".join(reversed(self.information['birthday'].split("/")))
        print(f"Birthday converted: {self.information['birthday']}")
        
        signup_res = post_sign_up(self.information)

        # Đưa thông tin gọi API
        if signup_res[0] == 400: # Sai thông tin
            self.signup_notification.text = "Tên đăng nhập đã tồn tại"
            print(f"SignUp Error: {self.signup_notification.text}")
            print(f"Infor: {self.information}")
        else: # Đăng nhập thành công
            # Thanh thông báo khi thành công
            self.signup_notification.text = "Đăng ký thành công"
            self.signup_notification.color = self.NOTIFI_SUCCESS_COLOR
            print(f"SignUp Completed: {self.signup_notification.text}")
            print(f"Infor: {self.information}")

            # Ẩn nút đăng nhập ở Home
            sign_in_button = self.parent.ids.home_page.ids.sign_in_button
            sign_in_button.text, sign_in_button.opacity, sign_in_button.disabled,sign_in_button.size_hint = "", 0, True, (0, 0)
            print("Changed sign in button in home page")

            login_res = login(
                {
                    'username' : self.information['username'], 
                    'password': self.information['password']
                }
            )
            if login_res[0] == 400: # Sai thông tin
                print("Login failed")
            else:
                print("Login successfully")
            token = login_res[1]['token']
            login_page = self.parent.ids.login_page
            login_page.user = self.information['username']
            login_page.access_token = token
            print("Updated user")

            history_button = self.parent.ids.home_page.ids.history_button
            history_button.disabled = False
            print("Enabled history button")

            print(signup_res[1]['id'])
            history_page = self.parent.ids.history_page
            history_page.update(token)
            print(history_page.access_token)
            history = history_page.ids.history
            history.update()
            print("Generated history")

            self.go_back() # Quay trở trang home

    def go_back(self, *args):
        # Trì hoãn chuyển trang
        Clock.schedule_once(self.change_screen, .5)

    def change_screen(self, dt):
        # Reset lại signup form khi đăng nhập thành công
        self.manager.current = 'home'
        self.manager.transition.direction = "up"
        self.signup_notification.text = ""
        self.ids.firstname.text = ""
        self.ids.lastname.text = ""
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.email.text = ""
        self.ids.birthday.text = ""