# 흥부와 놀부의 결과를 저장하기 위한 변수를 선언한다.
import random
import time

# 도, 개, 걸, 윷, 모 정의
def sum_stick(sticks) :
    score = sticks.count(0)
    if score == 0 :
        score = 5
    return score            

h = 0
n = 0

yut = ['', '도 (1점)', '개 (2점)', '걸 (3점)', '윷 (4점)', '모 (5점)']

# 누구의 차례인지 계산하기 위한 변수를 선언한다.
turn = True                        

# 게임 시작
while True:
    # 윷가락 변수 선언 및 초기화
    sticks = [0,0,0,0]
    # 윷을 던진다
    for i in range(4) :
        sticks[i] = random.randint(0,1) 

    # 도, 개, 걸, 윷, 모 호출
    score = sum_stick(sticks)

    # 해당 차례인 사람에게 결과를 저장한다.
    if turn : # turn = True
        h = h + score
        print(f'흥부 {sticks}: {yut[score]}/총{h}점 --->')
    else : 
        n = n + score
        print(f'\t\t\t\t <--- 놀부 {sticks}: {yut[score]}/총{n}점')
    
    # 윷이나 모가 나오면 턴을 변경하지 않는다.
    if score < 4 :
        if turn :
            turn = False
        else :
            turn = True

    # 점수가 20점 이상이면 게임 종료
    if h >= 20 or n >= 20 :
        break
    time.sleep(0.5)

# 결과를 출력한다. 
print(f'{'흥부' if h >= 20 else '놀부'} 승리 => 흥부: {h}, 놀부: {n}')


