## ------------------------------------------------
## 제작 정보 : 2025.07.10. KDT기 김미래
## 프로그램 이름 : 여행추천프로그램
## 프로그램 목적 : 원활한 여행 일정 관리
## 프로그램 기능
##  -> 회원 정보 입력
##  -> 메뉴 안내
##  -> 일정 입력
##  -> 교통편 선택
##  -> 여행 취향 선택
##  -> 음식 취향 선택
##  -> 숙소 취향 선택
##  -> 최종 여행 지역 추천
##  => 일정표 
## ------------------------------------------------
import random

info_list = []
summary = {
   "nickname": "",
   "location": "",
   "start_date" : 0,
   "end_date" : 0,
   "start_time": "",
   "vehicle":"",
   "trip_style" : "",
   "food_style": "",
   "food_type" : "",
   "food_menu" : [],
   "stay_type" : ""
}

def main() :
  print('\n')
  print(f'{"="*70}')
  print(f'{"😎 WELCOME TRAVELER!":^60}')
  print(f'{"="*70}')
  print('\n')

  print(f'{"="*70}')
  info = input("👉 닉네임? 👉 출발지? ")
  global info_list
  info_list = info.split()
  summary["nickname"] = info_list[0]
  summary["location"] = info_list[1]
  print(f'   {summary["location"]}사는 {summary["nickname"]}님! 환영합니다!😎')
  print(f'{"="*70}')

def welcome() :
    print(f'{"="*70}')
    print(f'{" 🪄🪄🪄  추천 프로세스🪄🪄🪄 ":^60}')
    print(f'{"="*70}')
    print(f' 1단계 → 2단계 → 3단계 → 4단계 → 5단계 → 일정추천')
    print(f'{"="*70}')

def menu():
    print('\n')
    print(f'{"="*70}')
    print(f'{" 🪄🪄🪄  메뉴 단계 안내 🪄🪄🪄 ":^60}')
    print(f'{"="*70}')
    print(f'{" [1단계] 여행 희망 일정":^10}')
    print(f'{" [2단계] 교통 취향 선택":^10}')
    print(f'{" [3단계] 여행 취향 선택":^10}')
    print(f'{" [4단계] 음식 취향 선택":^10}')
    print(f'{" [5단계] 숙소 취향 선택":^10}')
    print(f'{" [최 종] 여행 조합 추천":^10}')
    print(f'{"="*70}')
    
## ----------------------------------------------------
## [1단계] 여행 가능한 일정 입력
## - 함수이름 : date_menu
## - 매개변수 : start_date, end_date
## - 반   환 : 일정
## ----------------------------------------------------
def date_menu():

  while True :
    start_date = input(f"🧳 출발 일정(예: 250711 오전): ").split()
    if len(start_date[0]) == 6 and start_date[1] in ['오전', '오후']:
      summary["start_date"] = int(start_date[0])
      summary["start_time"] = start_date[1]
      summary["end_date"] = int(input(f"🧳 도착 일정(예: 250713): "))
      nights = summary["end_date"] - summary["start_date"]
      print(f'{"="*70}')
      print(f'👉 오~ {nights}박 {nights+1}일 {summary["start_time"]}출발 여행이야.😎')
      print(f'{"="*70}')
      return
    else :
      print(f'잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.')
      print(f'{"="*70}')
     

## ----------------------------------------------------
## [2단계] 교통편 선택하기
## - 함수이름 : vehicle_menu
## - 매개변수 : 없음
## - 반   환 : 
## ----------------------------------------------------
def vehicle_menu():
    print('\n')
    print(f'{"="*70}')
    print(f'{" 🪄🪄🪄  교통편 선택하기 🪄🪄🪄 ":^60}')
    print(f'{"="*70}')
    print(f'{" [1] 🚂 기차 [2] 🚌 버스 [3] 🚗 자동차":^60}')
    print(f'{"="*70}')

    
    # 숫자에 따른 교통편 매핑
    vehicle_map = {
        "1" : "🚂 기차",
        "2" : "🚌 버스",
        "3" : "🚗 자동차"
    }
    print(f'{"="*70}')

    while True :
      vehicle_choice = input(f" 뭐 타고 갈까?😏 (예: 1 또는 2 또는 3): ").strip()
      if vehicle_choice in vehicle_map :
        summary["vehicle"] = vehicle_map[vehicle_choice]
        print(f'{info_list[0]}님! {summary["vehicle"]}를 교통편으로 선택하셨군!')
        break    # 다음 단계로 이동    
      else:
        print(f'잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.')
        print(f'{"="*70}')

## ----------------------------------------------------
## [3단계] 여행 취향 선택하기
## - 함수이름 : trip_style_menu
## - 매개변수 : 없음
## - 반   환 : 
## ----------------------------------------------------
def trip_style_menu() :
    print('\n')
    print(f'{"="*70}')
    print(f'{" 🪄🪄🪄  여행 취향 선택하기 🪄🪄🪄 ":^60}')
    print(f'{"="*70}')
    print(f'{" [1] ☘️ 자연휴양 [2] 🍹카페투어 [3] 🎠액티비티 [4] 🚢 바다투어 ":^50}')
    print(f'{"="*70}')

    
    # 숫자에 따른 여행 취향 매핑
    style_map = {
        "1" : "☘️자연휴양",
        "2" : "🍹카페투어",
        "3" : "🎠액티비티",
        "4" : "🚢 바다투어"
    }
    print(f'{"="*70}')

    while True :
      style_choice = input(f" 여행 취향은 어때?😗(예: 1 또는 2 또는 3 또는 4): ").strip()

      if style_choice in style_map :
        summary["trip_style"] = style_map[style_choice]
        print(f'   {summary["nickname"]}님! 이제 {summary["trip_style"]}하러 떠나볼까!')
        break
      else:
        print(f'잘못된 선택입니다. 1, 2, 3, 4 중에서 선택해주세요.')
        print(f'{"="*70}')

## ----------------------------------------------------
## [4단계] 음식 취향 선택하기
## - 함수이름 : food_style_menu
## - 매개변수 : 없음
## - 반   환 : 
## ----------------------------------------------------
def food_style_menu() :
    print('\n')
    print(f'{"="*70}')
    print(f'{" 🪄🪄🪄  음식 취향 선택하기 🪄🪄🪄 ":^60}')
    print(f'{"="*70}')
    print(f'{" [1] 🍚 한식파 [2] 🥪 간단히 [3] 🧁디저트파 ":^60}')
    print(f'{"="*70}')

    food_map = {
    "1": ("🍚 한식파", [
        "김치찌개", "된장찌개", "청국장", "비빔밥", "불고기", "제육볶음", "순대국", "감자탕", "갈비탕", "설렁탕",
        "육개장", "떡볶이", "잡채", "오징어볶음", "쭈꾸미볶음", "부대찌개", "콩나물국밥", "해장국", "비빔국수", "냉면",
        "삼겹살", "닭갈비", "돼지불백", "계란찜", "계란말이", "갈비찜", "장어구이", "간장게장", "양념게장", "생선구이",
        "홍어삼합", "감자조림", "두부조림", "멸치볶음", "고등어조림", "갈치조림", "코다리찜", "소불고기", "닭볶음탕", "파전",
        "김치전", "해물파전", "순두부찌개", "묵은지찜", "오삼불고기", "소고기무국", "미역국", "무국", "시래기국", "북엇국",
        "장조림", "깻잎장아찌", "열무국수", "칼국수", "수제비", "잔치국수", "냉콩국수", "비빔칼국수", "해물칼국수", "떡국",
        "만둣국", "육전", "호박전", "고추전", "도토리묵", "청포묵", "우엉조림", "나물비빔밥", "산채비빔밥", "돌솥비빔밥",
        "영양밥", "곤드레밥", "쌈밥", "보쌈", "족발", "편육", "동태찌개", "아구찜", "굴국밥", "홍합탕", "매운탕",
        "동그랑땡", "비지찌개", "깍두기볶음밥", "김치볶음밥", "계란볶음밥", "참치김밥", "소고기김밥", "유부초밥", "김말이",
        "고로케", "부추전", "명란비빔밥", "계란덮밥", "연어덮밥", "장어덮밥", "김치찜", "두부김치", "묵사발", "열무비빔밥"
    ]),
    "2": ("🥪 간단히", [
        "샌드위치", "크로아상 샌드위치", "햄치즈샌드", "치킨랩", "햄버거", "핫도그", "치즈볼", "타코야키", "계란토스트", "김밥",
        "참치김밥", "계란김밥", "떡꼬치", "컵떡볶이", "순대", "호떡", "붕어빵", "잉어빵", "군고구마", "군밤",
        "군옥수수", "치킨너겟", "치즈스틱", "떡강정", "컵라면", "컵밥", "삼각김밥", "유부초밥", "감자튀김", "와플",
        "미니핫도그", "고로케", "토스트", "바게트샌드", "클럽샌드", "치킨까스샌드", "오니기리", "라이스페이퍼롤", "치킨버거", "오믈렛",
        "소세지빵", "피자빵", "핫바", "튀김우동컵", "미니도시락", "치킨도시락", "스팸무스비", "페퍼로니피자", "마가리타피자", "편의점토스트",
        "크랩롤", "참치롤", "야끼소바빵", "조각케이크", "핫초코", "라떼", "아이스트커피", "바나나우유", "요거트", "슈크림빵",
        "샐러드컵", "과일컵", "햄버거스낵랩", "김치전", "녹두전", "치즈돈까스랩", "핫치킨랩", "컵오징어", "소떡소떡", "만두컵",
        "미니핫도그컵", "마카로니샐러드", "에그샐러드", "베이글샌드", "치킨마요컵밥", "불닭마요", "불고기버거", "치킨마요삼각김밥", "고추참치삼각김밥", "초코우유",
        "두유", "커스터드빵", "콘샐러드컵", "참치마요컵밥", "닭강정컵", "에그타르트", "냉우동컵", "볶음밥컵", "소고기덮밥", "계란덮밥",
        "나초컵", "치킨봉", "훈제오리덮밥", "치킨현미랩", "크림치즈롤", "포테이토롤", "크림파스타컵", "치킨텐더", "연어롤", "핫윙"
    ]),
    "3": ("🧁 디저트파", [
        "티라미수", "브라우니", "마카롱", "휘낭시에", "에그타르트", "젤라또", "아이스크림", "와플", "빙수", "쿠키",
        "초코쿠키", "오트밀쿠키", "마들렌", "파운드케이크", "카스텔라", "딸기케이크", "생크림케이크", "레몬파이", "블루베리파이", "초코무스",
        "크렘브륄레", "푸딩", "요거트", "그릭요거트", "초코칩머핀", "블루베리머핀", "바나나머핀", "치즈케이크", "오레오치즈케이크", "크로캉부슈",
        "베이글크림", "크림샌드", "크로플", "슈", "몽블랑", "밀푀유", "젤리", "초코바", "생초콜릿", "카라멜팝콘",
        "팥빙수", "망고빙수", "녹차빙수", "카페모카", "카라멜마끼아또", "아포가토", "에스프레소젤라또", "브라우니아포가토", "생딸기크림", "초코브라우니볼",
        "미니도넛", "글레이즈드도넛", "찹쌀도넛", "팥도넛", "슈크림도넛", "롤케이크", "크림롤", "모찌롤", "찹쌀떡", "경단",
        "쑥떡", "인절미", "호떡", "꿀호떡", "옥수수빵", "단팥빵", "크림빵", "밀크바", "와우바", "초코칩아이스크림",
        "샤베트", "망고젤라또", "쫀득이", "마시멜로", "푸쉬팝", "롤리팝", "츄파춥스", "젤리빈", "하리보", "과일타르트",
        "바나나케이크", "피넛버터쿠키", "크림치즈푸딩", "쵸코마들렌", "에끌레어", "초코퐁당", "코코넛볼", "크림치즈브레드", "크로와상슈", "타르트타탱"
    ])
  }
    
    nights = summary["end_date"] - summary["start_date"]

    while True :
      food_choice = input(f" 여행에서 가장 중요한 음식 취향은?🤩 (1 또는 2또는 3): ").strip()
      if food_choice in food_map :
        style_name, food_list = food_map[food_choice]
        summary["food_type"] = style_name
        print(f'   {summary["nickname"]}님~ {summary["food_type"]}러버구나!')

        while True:
        # 랜덤 메뉴 추천 
          menu_count = min(nights+1, len(food_list))
          recommended_menu = random.sample(food_list, menu_count)
          print(f' 👉 추천 메뉴 : ')
          for i, menu in enumerate(recommended_menu, 1) :
            print(f' 👉 Day {i} 추천 메뉴 : {menu} ')
            
          confirm = input(f' 마음에 들어? (Y:선택 / N:다시 추천) : ').strip().lower()
          if confirm == 'y':
            summary["food_menu"] = recommended_menu
            print(f'\n{summary["food_menu"]}!!! 일정에 포함할게.😤')
            return #break_style_menu() # 다음 단계로 이동 
          else:
            print("그럼 다른 메뉴 추천한다! 🍽️")
      else : 
        print(f'잘못된 선택입니다. 1~3 중에서 골라주세요.')

      # style_name -> "🍚 한식파"
      # food_list -> ["비빔밥", "김치찌개"...]
      # food_map[food_choice][0] : "🍚 한식파"
      # food_map[food_choice][1] : ["비빔밥", "김치찌개"...]       
## ----------------------------------------------------
## [5단계] 숙소 취향 선택하기
## - 함수이름 : break_style_menu
## - 매개변수 : 없음
## - 반   환 : 
## ----------------------------------------------------
def break_style_menu():
    print('\n')
    print(f'{"="*70}')
    print(f'{" 🪄🪄🪄  숙소 취향 선택하기 🪄🪄🪄 ":^60}')
    print(f'{"="*70}')
    print(f'{" [1] 🏨 호텔 [2] 🏕️ 캠핑장 [3] 🛖게스트하우스 ":^60}')
    print(f'{"="*70}')

    stay_map = {
       "1":"🏨 호텔",
       "2":"🏕️ 캠핑장",
       "3":"🛖게스트하우스"
    }
    
    while True :
      stay_choice = input(" 어떤 숙소에서 쉬고 싶어?😴 (예: 1 또는 2또는 3): ").strip()
      if stay_choice in stay_map :
        summary["stay_type"] = stay_map[stay_choice]
        print(f'   {summary["nickname"]}님~ {summary["stay_type"]}에서 푹 쉬고 오자구요!🥱')
        break
      else :
        print(f'잘못된 선택입니다. 1, 2, 3 중에서 선택해주세요.')
        print(f'{"="*70}')

def final_summary() :
  nights = summary["end_date"] - summary["start_date"]
  print(f'{"="*70}')
  print(f'👉 이제 취향을 모두 반영해서 여행을 추천할게!🧳')
  print(f'{"="*70}')
  print(f'{summary["location"]}사는 {summary["nickname"]}님!, {nights}박 {nights+1}일 {summary["start_time"]}출발 여행이야.')
  print(f'{summary["vehicle"]}를 타고 {summary["trip_style"]}하자.')
  print(f'{summary["food_type"]}니까 {summary["food_menu"]}먹고 {summary["stay_type"]}에서 힐링해.')
  print(f'{"="*70}')

def recommended_arrival() :
  print(f'{"="*70}')
  print(f'{"🕰️ 도착지를 추천해볼게! ":^60}')
  print(f'{"="*70}')

  arrival_list = [
  "강릉", "속초", "춘천", "양양", "대전", "청주", "세종", "전주",
  "군산", "부안", "광주", "순천", "여수", "목포",
  "부산", "대구", "울산", "포항", "경주", "통영", "거제", "진주",
  "제주", "남해", "태안", "동해", "삼척" ]
  
  # 출발지 제외한 도착지 리스트
  filtered_arrivals = [place for place in arrival_list if place != info_list[1]]
  
  while True :
    arrival = random.choice(filtered_arrivals)
    print(f' ⭐ 오늘의 추천 여행지는 바로... ⭐ 👉 {arrival} 👈')
    confirm = input("   마음에 들어? (Y: 선택 / N: 다시 추천)").strip().lower()

    if confirm == 'y' :
       print(f'\n🌈 {arrival} 여행 떠나보자고! 😎\n')
       return arrival
    else:
       print('그럼 다른 곳으로 추천해볼게! 😤')


def print_schedule_with_time():
  nights = summary["end_date"] - summary["start_date"]

  print("\n" + "="*70)
  print(f'🧳  [{summary["start_time"]} 출발] {summary["nickname"]}님의 {nights}박 {nights + 1}일 {summary["food_type"]}여행 일정표 🧁 (교통: {summary["vehicle"]})')
  print("="*70)
  print("날짜       | 시간           | 일정내용")
  print("-"*70)


  for i in range(1, nights + 2):
      if i == 1:
            print(f"1일차(오전)| 08:00~09:00    | 기상 및 출발 준비")
            print(f"           | 09:00~12:00    | {summary['vehicle']} 출발 → 이동")
            print(f"           | 12:00~13:30    | 🍰 카페투어")
            print(f"           | 14:00~17:30    | 🎡 여행 취향 활동: {summary['trip_style']}")
            print(f"           | 18:00~19:30    | 🍽️ 추천 메뉴: {summary['food_menu'][0]}")
            print(f"           | 20:00~22:00    | {summary['stay_type']} 숙소 도착 및 휴식")
      elif i == nights + 1:
            print(f"{i}일차      | 08:00~09:00    | 기상 및 체크아웃")
            print(f"           | 09:00~12:00    | 🛤️ 이동 및 귀가")
      else:
            print(f"{i}일차      | 08:00~09:00    | 기상 및 산책")
            print(f"           | 09:00~12:00    | 🎡 여행 취향 활동: {summary['trip_style']}")
            print(f"           | 12:00~13:30    | 🍽️ 추천 메뉴: {summary['food_menu'][i-1]}")
            print(f"           | 14:00~17:30    | 자유시간 또는 명소 방문")
            print(f"           | 18:00~19:30    | 저녁 식사 및 기념품 쇼핑")
            print(f"           | 20:00~22:00    | {summary['stay_type']} 숙소 휴식")
      print("-"*70)

  print(f"🎉 {summary['nickname']}님만을 위한 맞춤 일정! 즐거운 여행 되세요~!")
  print("="*70)



def run_travel_program() :
  main()
  welcome()
  menu()
  date_menu()
  vehicle_menu()
  trip_style_menu()
  food_style_menu()
  break_style_menu()
  final_summary()
  recommended_arrival()
  print_schedule_with_time()

if __name__ == "__main__":
    run_travel_program()