# card.py
# Card 클래스: 한 장의 카드를 표현

class Card:
    def __init__(self, card_suit, card_number):
        self.suit = card_suit
        self.number = card_number

    def __str__(self):
        # print(card) 호출 시
        return f'({self.suit},{self.number:>2})'

    def __repr__(self):
        # 카드 형태로 출력
        return self.__str__()
