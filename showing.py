from utils import *

class Movies(StackLayout):
    movies = get_movies() # Lấy list movie
    movie_ids = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Hằng số thuộc tính
        FILM_ROW_NUM = ceil(len(self.movies) / 4) # Số hàng phim

        # Điều chỉnh thuộc tính
        self.height = dp(FILM_ROW_NUM * 500) 

        # Tạo components
        for movie in self.movies:
            # Hộp phim
            boxlayout = BoxLayout(orientation='vertical', size_hint=(.25, 1 / FILM_ROW_NUM))
            # Ảnh phim
            boxlayout.add_widget(ImageButton(source=movie['posterURL'], size_hint=(1, .8), pos_hint={'center_x': .5}))
            # Tên phim
            boxlayout.add_widget(Label(text=movie['title'],  size_hint=(1, .15), color=(0, 0, 0), font_size=dp(15), font_name='assets/fonts/Roboto-Medium.ttf'))
            # Nút đặt vé
            button = Button(text="Đặt vé",  size_hint=(.5, .05), pos_hint={'center_x': .5}, font_name='assets/fonts/Kanit-Medium.ttf', 
                                        on_press=lambda instance, movie_ref=movie: self.update_movie(instance, movie_ref), 
                                        on_release=self.go_to_movie_detail)
            self.movie_ids[button] = str(movie['id'])
            boxlayout.add_widget(button)
            
            self.add_widget(boxlayout)

    def update_movie(self, button, movie):
        # Gọi thông tin tên phim
        detail_movie = get_movie_detail(self.movie_ids[button])
        
        # Lấy root: WindowManager
        window_manager = self.parent.parent.parent.parent.parent

        # Lấy movie_detail từ DeatailWindow
        movie_detail = window_manager.ids.detail_page.ids.movie_detail
        movie_detail.update(detail_movie) # Truyền tên phim

        # Lấy date_area từ DetailWindow và cập nhật phim
        schedule = get_screening(self.movie_ids[button])
        date_area = window_manager.ids.detail_page.ids.date_area
        date_area.update(schedule, movie['title']) # Truyền lịch cho DateArea
        
    def go_to_movie_detail(self, instance):
        self.parent.parent.parent.parent.manager.current = "detail"
        self.parent.parent.parent.parent.manager.transition.direction = "up"

class ShowingWindow(Screen):
    pass
    