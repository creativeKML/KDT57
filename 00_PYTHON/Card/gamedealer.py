# gamedealer.py
# GameDealer 클래스: 덱 생성, 셔플, 분배, 출력

import random
from card import Card

class GameDealer:
    def __init__(self):
        self.deck = []          # 딜러가 가진 카드 리스트
        self.suit_number = 13   # 무늬별 카드 수

    def make_deck(self):
        # 52장 덱 생성
        self.deck.clear()
        card_suits = ["♠", "♥", "♣", "◆"]
        card_numbers = ["A", "2", "3", "4", "5", "6", "7",
                        "8", "9", "10", "J", "Q", "K"]
        for s in card_suits:
            for n in card_numbers:
                self.deck.append(Card(s, n))

    def shuffle_deck(self):
        # 덱 랜덤 셔플
        random.shuffle(self.deck)

    def distribute_card(self, players, num=10):
        # 각 Player에게 num장씩 나눠주고 deck에서 제거
        print("=" * 60)
        print(f"카드 나누어 주기: {num}장")
        print("-" * 60)
        for p in players:
            taken = self.deck[:num]
            del self.deck[:num]
            p.add_card_list(taken)
        # 분배 후 딜러 덱 상태 출력
        self.display_deck()

    def display_deck(self):
        # 덱의 내용 출력 (한 줄에 13장씩)
        print(f"[GameDealer] 딜러가 가진 카드 수: {len(self.deck)}")
        for i, c in enumerate(self.deck, 1):
            print(c, end="\t")
            if i % 13 == 0:
                print()
        if len(self.deck) % 13 != 0:
            print()
