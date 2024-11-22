import requests

BASE_URL = 'http://localhost:8080/cinemabooking/'
MOVIES_PATH = 'movie'
MOVIES_DETAIL_PATH = '/movies/detail/'
SEATS_PATH = 'screening/seats/'
LOGIN_PATH = 'auth/login'
BOOKING_PATH = 'booking/book'
SCREENING_PATH = 'screening/movie/'

# Trả về phim đang chiếu
def get_movies():
    try: 
        # Chỉ trả về list movie
        response = requests.get(BASE_URL + MOVIES_PATH)
        
        return response.json()
    except:
        print("GET API FAILED")


# Trả về phim cụ thể
def get_movie_detail(id):
    try:
        return requests.get(BASE_URL + MOVIES_PATH + '/' + id).json()['result']
    except:
        print("GET API FAILED")


# Trả về ngày và thời gian chiếu
def get_screening(id):
    try:
        return requests.get(BASE_URL + SCREENING_PATH + id).json()['result']['screenings']
    except:
        print("GET API FAILED")


# Trả về vé và chỗ ngồi đã đặt
def get_seats(screening_id, token = None):
    try:
        headers = {
            'Authorization': f'Bearer {token}',
        }
        return requests.get(BASE_URL + SEATS_PATH + screening_id, headers=headers).json()['result']['bookedSeats']
    except:
        print('POST API FAILED')
print(get_seats('35f8a73f-e86c-48ea-9e42-5599900ed937', 
                'eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJodXluaGNhbmh2aWVuIiwic3ViIjoia2hvYTI1MDYwNSIsImV4cCI6MTczMjI1NDc1NywiaWF0IjoxNzMyMjUxMTU3LCJqdGkiOiJiNjA1NWVmZC02OTJkLTQ5ZGUtYWI3ZS1hYWU5ZGI3NDE4MWYiLCJzY29wZSI6IlVTRVIifQ.lEGl053jAZi6SoVJALwS9PTJDSVqaIKskL1TWUKcUuLpmUeeBzhi9hYJWGaR04RUFYvmYfwkENloUUa5FCiuvw'))

# Đăng nhập
def login(data):
    try:
        response = requests.post(BASE_URL + LOGIN_PATH, json=data)
        result = response.json()
        if response.status_code == 400:
            return (response.status_code, result['message'])
        return (response.status_code, result['result'])
    except:
        print("LOGIN FAILED")


# Đặt vé:
def booking(data, token = None):
    try:
        headers = {
            'Authorization': f'Bearer {token}',
        }
        response = requests.post(BASE_URL + BOOKING_PATH, json=data, headers=headers)
        return response
    except:
        print("BOOKING FAILED")

    
# Lấy lịch sử đặt vé
def get_booking_history(token = None):
    try:
        headers = {
            'Authorization': f'Bearer {token}',
        }
        response = requests.get('http://localhost:8080/cinemabooking/user/myBookings', headers=headers)
        print("GET HISTORY SUCCESSFULLY")
        return response.json()['result']
    
    except:
        print("GET API FAILED")
        return []

def post_sign_up(infor: dict):
    try:
        response = requests.post('http://localhost:8080/cinemabooking/user', json=infor)
        result = response.json()
        if response.status_code == 400:
            print(result['message'])
            return (response.status_code, result['message'])
        print(result['result'])
        return (response.status_code, result['result'])
    except:
        print("SiGN UP FAILED")