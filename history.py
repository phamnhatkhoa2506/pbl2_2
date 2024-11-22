from utils import *

class History(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self):
        self.clear_widgets()
        print(self.parent.parent.parent.parent)
        self.booking_history = get_booking_history(self.parent.parent.parent.parent.access_token)
        print(f"History: {self.booking_history}")
        self.height = (len(self.booking_history) + 1) * dp(100) + len(self.booking_history) * dp(50)
        self.spacing = dp(50)

        title_layout = BoxLayout(orientation='horizontal', size_hint_y=None)
        title_layout.add_widget(Label(text='Đặt lúc', color=(0, 0, 0)))
        title_layout.add_widget(Label(text='Tổng giá', color=(0, 0, 0)))
        title_layout.add_widget(Label(text='Phim', color=(0, 0, 0)))
        title_layout.add_widget(Label(text='Thời gian chiếu', color=(0, 0, 0)))
        title_layout.add_widget(Label(text='Rạp', color=(0, 0, 0)))
        title_layout.add_widget(Label(text='Ghế', color=(0, 0, 0)))
        self.add_widget(title_layout)

        for booking in self.booking_history:
            booking_layout = BoxLayout(orientation='horizontal', size_hint_y=None)
            booking_layout.add_widget(Label(text=booking["bookedDate"] + ' ' + booking["bookedTime"][:8:], color=(0, 0, 0)))
            booking_layout.add_widget(Label(text=str(int(booking["price"])) + ' VNĐ', color=(0, 0, 0)))
            booking_layout.add_widget(Label(text=booking["screeningResponse"]["movieName"], color=(0, 0, 0), size_hint_x=1))
            booking_layout.add_widget(Label(text=booking["screeningResponse"]["dateShow"] + ' ' + booking["screeningResponse"]["startTime"], color=(0, 0, 0)))
            booking_layout.add_widget(Label(text=booking["screeningResponse"]["theaterName"], color=(0, 0, 0)))
            booking_layout.add_widget(Label(text=", ".join(booking['seatCodes']),  color=(0, 0, 0)))

            self.add_widget(booking_layout)
        

class HistoryWindow(Screen):
    access_token = None

    def update(self, access_token):
        self.access_token = access_token
