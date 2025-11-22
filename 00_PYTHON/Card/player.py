# player.py
# Player 클래스: 받은 카드(holding)로 보관
# open/holding 두 리스트 출력 + 짝 맞추기 기능

class Player:
    def __init__(self, name):
        self.name = name
        self.holding_card_list = []   # 손에 들고 있는 카드
        self.open_card_list = []      # 짝 맞춘 카드

    def add_card_list(self, card_list):
        # GameDealer가 준 카드 holding 리스트에 추가
        self.holding_card_list.extend(card_list)

    def display_two_card_list(self):
        # 두 개 리스트 출력
        print("=" * 60)
        print(f"[{self.name}] Open card list: {len(self.open_card_list)}")
        if self.open_card_list:
            for i, card in enumerate(self.open_card_list, 1):
                print(card, end="\t")
                if i % 13 == 0:
                    print()
            if len(self.open_card_list) % 13 != 0:
                print()
        else:
            print("(없음)")

        print(f"\n[{self.name}] Holding card list: {len(self.holding_card_list)}")
        if self.holding_card_list:
            for i, card in enumerate(self.holding_card_list, 1):
                print(card, end="\t")
                if i % 13 == 0:
                    print()
            if len(self.holding_card_list) % 13 != 0:
                print()
        else:
            print("(없음)")

    def check_one_pair_card(self):
        number_to_cards = {}
        for card in self.holding_card_list:
            number_to_cards.setdefault(card.number, []).append(card)

        to_open = []

        for number, cards in number_to_cards.items():
            while len(cards) >= 2:  # 같은 번호 카드가 두 장 이상일 때
                c1 = cards.pop()
                c2 = cards.pop()
                to_open.extend([c1, c2])
                # holding_card_list 에서 제거
                self.holding_card_list.remove(c1)
                self.holding_card_list.remove(c2)

        # open_card_list 로 옮기기
        self.open_card_list.extend(to_open)
