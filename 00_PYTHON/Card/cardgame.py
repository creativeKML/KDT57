# cardgame.py
from player import Player
from gamedealer import GameDealer

def play_game():
    # 플레이어 생성
    player1 = Player("흥부")
    player2 = Player("놀부")
    players = [player1, player2]

    # 딜러 생성
    dealer = GameDealer()

    # 덱 생성 및 출력
    print("=" * 60)
    print("[GameDealer] 초기 카드 생성")
    dealer.make_deck()
    dealer.display_deck()

    # 덱 셔플 후 출력
    print("\n[GameDealer] 카드 랜덤하게 섞기")
    dealer.shuffle_deck()
    dealer.display_deck()

    # 각 Player에게 10장씩 분배
    dealer.distribute_card(players, 10)

    # 각 Player의 카드 상태 출력
    for p in players:
        p.display_two_card_list()

    # 같은 번호 카드 확인
    for p in players:
        p.check_one_pair_card()

if __name__ == "__main__":
    play_game()
