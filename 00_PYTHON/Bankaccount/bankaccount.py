# Python 클래스 활용 과제#1

class BankAccount :
    def __init__(self, name) :
        self.name = name
        self.__balance=0

    def deposit(self, amount) : # 입금
        self.__balance = self.__balance + amount
        print(f'{amount}원 입금: 통장 잔액 : {self.__balance}')

    def withdraw(self,amount) : # 출금
        if amount % 10000 != 0 : # 입력오류
            print(f'[입력 오류] 10000원 단위로 다시 입력하세요.')
        elif amount > self.__balance :
            print(f'통장 잔액이 부족합니다. 통장 잔액 : {self.__balance}')
        else : 
            self.__balance = self.__balance - amount 
            print(f'{amount}원 출금, 통장 잔액: {self.__balance}')

    def print_balance(self) :
        print(f'{self.name}, 잔액: {self.__balance}원')

    def run(self) :
        while True:
            print('-'*10)
            print(f'1. 입금')
            print(f'2. 출금')
            print(f'3. 조회')
            print(f'4. 종료')
            print('-'*10)

            try:
                menu_choice = int(input(f'메뉴 선택: '))

                if menu_choice == 1 :
                    amount = int(input(f'입금할 금액을 10000원 단위로 입력하세요: '))
                    self.deposit(amount)

                elif menu_choice == 2 :
                    amount = int(input(f'출금할 금액을 10000원 단위로 입력하세요: '))
                    self.withdraw(amount)            
    
                elif menu_choice == 3 :
                    self.print_balance()

                elif menu_choice == 4 :
                    print(f'프로그램을 종료합니다.')
                    break

                else:
                    print(f'잘못된 메뉴 선택입니다. 다시 입력하세요.')

            except ValueError :
                print('숫자를 입력하세요.')


account = BankAccount("KDT 은행")  # KDT 은행
account.run()
