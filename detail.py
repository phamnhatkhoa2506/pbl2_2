from utils import *

class MovieDetail(BoxLayout):
    movie = None

    # Thông tin phim truyền qua file .kv
    name_vn = StringProperty('')
    image = StringProperty('')
    type_vn = StringProperty('')
    time = StringProperty('')
    country_vn = StringProperty('')
    language_vn = StringProperty('')
    limitage_vn = StringProperty('')
    actor = StringProperty('')
    director = StringProperty('')
    brief_vn = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(minimum_height=self.setter('height')) # Ràng buộc chiều cao theo các components

    def update(self, movie):
        self.movie = movie

        # Cập nhật thông tin
        self.name_vn = movie['title']
        self.image = movie['posterURL']
        self.type_vn = movie['genre']
        self.time = f"{movie['duration']}"
        self.country_vn = movie["country"]
        self.language_vn = movie["language"]
        self.limitage_vn = str(movie['for_age'])
        self.actor = "Tham gia bởi nhiều ngôi sao lồng tiếng"
        self.director = 'Hayao Miyazaki'
        self.brief_vn = movie['description']

    # Điều chỉnh sự xuất hiện của các vùng đặt
    def justify_area(self, main_widget, height):
        root = self.parent.parent.parent.parent
        for widget in [root.ids.date_area, root.ids.time_area, root.ids.ticket_area, root.ids.seat_area]:
            if widget != main_widget or widget.height != dp(0):
                widget.height, widget.opacity, widget.disabled = dp(0), 0, True
            else:
                widget.height, widget.opacity, widget.disabled = dp(height), 1, False


class DateArea(BoxLayout):
    dates_dict = {} # Dict để lưu button theo string ngày tháng
    selected_date = ''
    selected_date_label = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update(self, schedule, movie_name):
        # Reset
        self.clear_widgets() # Xoá hết widgets trước khi tạo lại
        self.dates_dict = {}
        self.selected_date = ''
        self.selected_date_label = ''
        self.schedule = schedule

        # Tạo lại DateArea
        dates = [date for date in schedule.keys()]
        dates_area = BoxLayout(orientation="horizontal", size_hint_x=None, width=dp(len(dates)*200))
        for date in dates:
            date_str = str(date).split('-')
            date_str.reverse()
            date_str = "/".join(date_str)
            layout = RelativeLayout()
            button = Button(text=date_str,
                            size_hint=(.7, .3),
                            pos_hint={'center_x': .5, 'center_y': .5},
                            on_press=lambda _, d=date, t=schedule[date]: self.update_time(d, t, movie_name),
                            background_color=(64/255, 64/255, 64/255),
                            font_name='assets/fonts/Kanit-Bold',
                            font_size=dp(20))
            layout.add_widget(button)
            self.dates_dict[date_str] = button
            dates_area.add_widget(layout)

        all_area = BoxLayout(orientation='horizontal')
        all_area.add_widget(Label(text=''))
        all_area.add_widget(dates_area)
        all_area.add_widget(Label(text=''))

        self.add_widget(all_area)

    def update_time(self, date, time, movie_name):
        # Tạo màu sắc cho nút được nhấn
        if self.selected_date: # Nếu chưa có nút nào được nhấn
            self.dates_dict[self.selected_date].background_color = (64/255, 64/255, 64/255)
        date_str = str(date).split('-'); date_str.reverse(); date_str = "/".join(date_str) # Tạo xâu ngày tháng năm theo dạng dd/mm/yyyy

        self.dates_dict[date_str].background_color = (1, 1, 0) # Nút được nhấn đổi màu
        self.selected_date = date_str # Gán lại nút được nhấn cho nút được nhấn trước đó
        self.selected_date_label =  f"Ngày tháng chiếu: {date_str}\n"

        detail_window = self.parent.parent.parent.parent.parent # Lấy DetailWindow
        time_area = detail_window.ids.time_area
        time_area.update(time, movie_name) # Cập nhật TimeArea


class TimeArea(BoxLayout):
    times_dict = {}
    selected_time = ''
    selected_time_label = StringProperty('')
    selected_screening = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Hãy chọn ngày chiếu trước.', font_size=dp(30), color=(0, 0, 0))) # Label lúc chưa chọn ngày chiếu

    def update(self, this_times, movie_name):
        # Reset
        self.clear_widgets() # Xoá hết widgets trước khi tạo lại

        #  Tạo lại widgets
        times_area = BoxLayout(orientation="horizontal", size_hint_x=None, width=dp(len(this_times)*150))
        for time in this_times:
            time_str = time['startTime'][:5:]
            layout = RelativeLayout()
            button = Button(text=time_str,
                            size_hint=(.5, .3),
                            pos_hint={'center_x': .5, 'center_y': .5},
                            on_press=lambda _, t=time: self.update_ticket_and_seat(t, movie_name),
                            background_color=(64/255, 64/255, 64/255),
                            font_name='assets/fonts/Kanit-Bold',
                            font_size=dp(20))
            layout.add_widget(button)
            self.times_dict[time_str] = button
            times_area.add_widget(layout)
        
        all_area = BoxLayout(orientation='horizontal')
        all_area.add_widget(Label(text=''))
        all_area.add_widget(times_area)
        all_area.add_widget(Label(text=''))

        self.add_widget(all_area)
    
    def update_ticket_and_seat(self, time, movie_name):
        # Tạo màu sắc nút được chọn
        if self.selected_time: # Nếu chưa có nút nào được chọn
            self.times_dict[self.selected_time].background_color = (64/255, 64/255, 64/255)
        time_str = time['startTime'][:5:] # Chỉ lấy giờ và phút
        self.times_dict[time_str].background_color = (1, 1, 0) # Cập nhật màu cho nút được nhấn
        self.selected_time = time_str # Gán laị nút được nhấn cho nút được nhấn trước đó
        self.selected_time_label = f"Thời gian chiếu: {time_str}\n" 
        self.selected_screening = time['screeningId']

        detail_window = self.parent.parent.parent.parent.parent # Lấy DetailWindow

        ticket_area = detail_window.ids.ticket_area  # Lấy TicketArea
        ticket_area.update({
            "ticket_type": "Vé cho mọi lứa tuổi",
            "seat_type": "Đơn",
            "price": int(detail_window.ids.movie_detail.movie['price'])
        }) # Cập nhật TicketArea

        token = self.parent.parent.parent.parent.parent.parent.ids.login_page.access_token
        print(f"Token: {token}")

        seats_occupied = get_seats(time['screeningId'], token)
        print(f"Seat occupied: {seats_occupied}")
        seat_area = detail_window.ids.seat_area # Lấy SeatArea
        seat_area.update(time['theaterName'], seats_occupied) # Cập nhật SeatArea


class TicketArea(BoxLayout):
    # Biến
    total_num_tickets = 0
    total_cost = 0
    total_cost_label = StringProperty(str(total_cost))
    selected_tickets = set()
    selected_tickets_label = StringProperty('')

    # Hằng
    FONT_NAME='assets/fonts/Kanit-Bold'
    FONT_SIZE=dp(20)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Hãy chọn thời gian chiếu trước',  color=(0, 0, 0), font_size=dp(30))) # Label trước khi chọn thời gian chiếu

    def update(self, ticket_group):
        # Reset lại vùng thông tin
        self.clear_widgets() # Xoá hết widgets trước khi tạo lại
   
        # Tạo lại widgets
        ticket_area = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(len(ticket_group)*300))
        ticket_type = ticket_group['ticket_type']
        seat_type = ticket_group['seat_type']
    
        counting_area = BoxLayout(orientation='horizontal')
        count_label = Label(text=str(self.total_num_tickets), color=(0, 0, 0), font_size=self.FONT_SIZE, font_name=self.FONT_NAME)
        counting_area.add_widget(Button(text="-", size_hint_x=.2, font_name=self.FONT_NAME, background_color=(64/255, 64/255, 64/255), on_press=lambda _, tkg=ticket_group, cl=count_label: self.decrease(tkg, cl)))
        counting_area.add_widget(count_label)
        counting_area.add_widget(Button(text="+", size_hint_x=.2, font_name=self.FONT_NAME, background_color=(64/255, 64/255, 64/255), on_press=lambda _, tkg=ticket_group, cl=count_label: self.increase(tkg, cl)))

        ticket_box = BoxLayout(orientation="vertical", size_hint=(.7, .5), pos_hint={'center_x': .5, 'center_y': .5})
        ticket_box.add_widget(Label(text=ticket_type, color=(0, 0, 0), font_size=self.FONT_SIZE, font_name=self.FONT_NAME))
        ticket_box.add_widget(Label(text=seat_type, color=(0, 0, 0), font_size=self.FONT_SIZE, font_name=self.FONT_NAME))
        ticket_box.add_widget(Label(text=str(ticket_group['price']), color=(0, 0, 0), font_size=self.FONT_SIZE, font_name=self.FONT_NAME))
        ticket_box.add_widget(counting_area)
    
        layout = RelativeLayout()
        layout.add_widget(ticket_box)
        ticket_area.add_widget(layout)

        self.add_widget(Label(text=''))
        self.add_widget(ticket_area)
        self.add_widget(Label(text=''))

    def increase(self, ticket, count_label):
        self.total_num_tickets += 1 # Tăng tổng số lượng vé
        self.total_cost += ticket['price'] # Tăng tổng giá
        self.total_cost_label = str(self.total_cost) # Thay đổi label total cost
        self.selected_tickets_label = f"Số lượng vé: {self.total_num_tickets}\n" # Cập nhật label
        count_label.text = str(self.total_num_tickets) # Hiển thị số lượng vé lên app

        seat_area = self.parent.parent.parent.parent.parent.ids.seat_area # Lấy SeatArea
        if len(seat_area.selected_seats) > 0: # Nếu đã chọn ghế thì reset lại các ghế 
            seat_area.reset_seat()

    def decrease(self, ticket, count_label):
        if self.total_num_tickets > 0:
            self.total_num_tickets -= 1 # Trừ đi 1 tổng số vé
            self.total_cost -= ticket['price'] # Trừ đi tổng giá
            self.total_cost_label = str(self.total_cost) # Thay đổi label total cost
        count_label.text = str(self.total_num_tickets) # Thay đổi label vé
 
        self.selected_tickets_label = f"Số lượng vé: {self.total_num_tickets}\n" # Cập nhật label

        seat_area = self.parent.parent.parent.parent.parent.ids.seat_area # Lấy SeatArea
        if len(seat_area.selected_seats) > 0: # Nếu đã chọn ghế thì reset lại các ghế
            seat_area.reset_seat()


class SeatArea(BoxLayout):
    # Biến
    seats = {}
    selected_seats = set()
    selected_seats_label = StringProperty('')

    # Hắng thuộc tính
    SELECTED_SEAT_COLOR = (1, 0, 1)
    UNOCCUPIED_SEAT_COLOR = (.2, .2, .2)
    OCCUPIED_SEAT_COLOR = (.7, .2, .2)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='Hãy chọn thời gian chiếu trước', color=(0, 0, 0), font_size=dp(30))) # Label trước khi chọn thời gian chiếu

    def update(self, room_name, seats_occupied):
        self.clear_widgets() # Xoá hết widgets trước khi tạo
        self.room = room_name
        seats_occupied = set(seats_occupied) # Set các ghế đã được đặt trước
            
        # Tên rạp
        self.add_widget(Label(text=f"Rạp {self.room}", color=(0, 0, 0), size_hint=(.1, .1), pos_hint={'center_y': .9}, font_size=dp(30), font_name='assets/fonts/Kanit-Bold.ttf'))

        # Tạo khu vực các ghế
        all_seat_area = BoxLayout(orientation="vertical")
        col_index_area = BoxLayout(orientation="horizontal", size_hint=(1, .2))
        col_index_area.add_widget(Label(text=''))
        seat_area = BoxLayout(orientation="vertical")
        for i in range(1, 9):
            col_index_area.add_widget(Label(text=str(i), color=(0, 0, 0)))
            if i == 4:
                col_index_area.add_widget(Label(text='', size_hint_x=.25))
            i += 1
        for row in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
            row_area = BoxLayout(orientation="horizontal")
            row_area.add_widget(Label(text=row, color=(0, 0, 0)))
            
            for col in range(1, 5):
                layout = RelativeLayout()
                seat = Button(text=f"{row}{col}", background_color=(.2, .2, .2), on_press=self.get_seat)
                if seat.text in seats_occupied:
                    seat.background_color = self.OCCUPIED_SEAT_COLOR
                    seat.disabled = True
                layout.add_widget(seat)
                self.seats[f"{row}{col}"] = seat
                row_area.add_widget(layout)
            row_area.add_widget(Label(text='', size_hint_x=.25))
            for col in range(5, 9):
                layout = RelativeLayout()
                seat = Button(text=f"{row}{col}", background_color=(.2, .2, .2), on_press=self.get_seat)
                if seat.text in seats_occupied:
                    seat.background_color = self.OCCUPIED_SEAT_COLOR
                    seat.disabled = True
                layout.add_widget(seat)
                self.seats[f"{row}{col}"] = seat
                row_area.add_widget(layout)
            seat_area.add_widget(row_area)
        all_seat_area.add_widget(col_index_area)
        all_seat_area.add_widget(seat_area)
        self.add_widget(all_seat_area)
    
    # Thay đổi màu sắc cho ghê được chọn và thêm ghế được chọn
    def get_seat(self, instance):
        # Kiểm tra coi có mua đủ vé chưa
        root = self.parent.parent.parent.parent.parent
        if root.ids.ticket_area.total_num_tickets == len(self.selected_seats):
            if instance.text in self.selected_seats: # Ghế này chưa được cho vài
                self.selected_seats.remove(instance.text)
                instance.background_color = self.UNOCCUPIED_SEAT_COLOR
            self.selected_seats_label = f'Ghế đã chọn: Rạp {self.room} | {", ".join(self.selected_seats)}' # Cập nhật label
            return 
        
        if instance.text not in self.selected_seats: # Ghế này chưa được cho vài
            self.selected_seats.add(instance.text)
            instance.background_color = self.SELECTED_SEAT_COLOR
        else: # Ghế này có rồi, xoá ghế
            self.selected_seats.remove(instance.text)
            instance.background_color = self.UNOCCUPIED_SEAT_COLOR
        
        self.selected_seats_label = f'Ghế đã chọn: Rạp {self.room} | {", ".join(self.selected_seats)}' # Cập nhật label

    # Xoá hết cấc ghế đã chọn
    def reset_seat(self):
        for seat in self.selected_seats:
            self.seats[seat].background_color = self.UNOCCUPIED_SEAT_COLOR
        self.selected_seats.clear()
        self.selected_seats_label = 'Ghế đã chọn: '


class TotalArea(BoxLayout):
    pass


class DetailWindow(Screen):
    # Reset lại mọi thứ khi thoát ra khỏi trang
    def on_leave(self, *args):
        date_area = self.ids.date_area
        time_area = self.ids.time_area
        ticket_area = self.ids.ticket_area
        seat_area = self.ids.seat_area
        note_area = self.ids.note

        time_area.times_dict = {}
        time_area.selected_time = ''
        time_area.selected_time_label = ''
        ticket_area.total_num_tickets = 0
        ticket_area.total_cost = 0
        ticket_area.total_cost_label = '0'
        ticket_area.selected_tickets = set()
        ticket_area.selected_tickets_label = ''
        seat_area.seats = {}
        seat_area.selected_seats = set()
        seat_area.selected_seats_label = ''
        note_area.text = "Hãy chọn thông tin đặt vé"

        date_area.clear_widgets()
        time_area.clear_widgets()
        ticket_area.clear_widgets()
        seat_area.clear_widgets()
        
        time_area.add_widget(Label(text="Hãy chọn ngày chiếu trước", font_size=dp(30), color=(0, 0, 0)))
        ticket_area.add_widget(Label(text="Hãy chọn thời gian chiếu trước", font_size=dp(30), color=(0, 0, 0)))
        seat_area.add_widget(Label(text="Hãy chọn thời gian chiếu trước", font_size=dp(30), color=(0, 0, 0)))
        
        if date_area.disabled == True:
            date_area.height, date_area.opacity, date_area.disabled = dp(200), 1, False
        if time_area.disabled == False:
            time_area.height, time_area.opacity, time_area.disabled = dp(0), 0, True
        if ticket_area.disabled == False:
            ticket_area.height, ticket_area.opacity, ticket_area.disabled = dp(0), 0, True
        if seat_area.disabled == False:
            seat_area.height, seat_area.opacity, seat_area.disabled = dp(0), 0, True

    def booking(self):
        login_page = self.parent.ids.login_page
        date_area = self.ids.date_area
        time_area = self.ids.time_area
        ticket_area = self.ids.ticket_area
        seat_area = self.ids.seat_area
        note_area = self.ids.note

        selected_seats = seat_area.selected_seats
        
        if date_area.selected_date == "":
            note_area.text = "Bạn phải chọn ngày tháng chiếu"
            return
        if time_area.selected_time == "":
            note_area.text = "Bạn phải chọn thời gian chiếu"
            return
        if not ticket_area.total_num_tickets:
            note_area.text = "Bạn phải thêm số lượng vé"
            return
        if not len(selected_seats):
            note_area.text = "Bạn phải chọn chỗ ngồi"
            return
        if len(selected_seats) < ticket_area.total_num_tickets:
            note_area.text = "Bạn phải chọn số lượng ghế ứng với số lượng vé đã đặt"
            return
        if not login_page.user:
            note_area.text = "Bạn phải đăng nhập để đặt vé"
            return
        
        data = { 
            "screeningId": time_area.selected_screening ,
            "seatCodes": list(seat_area.selected_seats)
        }

        print(data)

        token = self.parent.ids.login_page.access_token
        detail = booking(data, token)
        print(detail)

        self.manager.current = 'home'
        self.manager.transition.direction = "down"

        self.parent.ids.history_page.ids.history.update()
        print("updated history")
        
