'''
은행 계좌 관리: class 활용 ver1
'''

class BankAccount:  # name = 'Bank'
	def __init__(self, name):
		self.balance= 0
		self.bank_name = name
		# 생성자에서 메뉴 바로 시작 
		#self.run()

	def withdraw(self, amount):
		'''
		10000원 단위 출금 함수 
		'''
		if amount % 10000 == 0:
			if self.balance < amount:
				print(f"통장 잔액이 부족합니다. 통장 잔액: {self.balance:,}원")
			else:		
				self.balance -= amount
				print(f"{amount:,}원 출금, 통장 잔액: {self.balance:,}원")
		else:
			print('[입력 오류] 10000원 단위로 다시 입력하세요.')
		
		
	def deposit(self, amount):
		'''
		10000원 단위 입금 함수 
		'''
		if amount > 0 and amount % 10000 == 0:			
			self.balance+= amount
			print(f"{amount:,}원 입금, 통장 잔액: {self.balance:,}원")
		else:
			print('[입력 오류] 10000원 단위로 다시 입력하세요.')
		

	def print_balance(self):
		'''
		통장 잔액 출력 
		'''
		print(f'{self.bank_name}, 잔액: {self.balance:,}원')


	def run(self):		
		'''
		입출금 동작 함수 
		'''
		while(True):
			print('------------')
			print(f'{self.bank_name}')
			print('------------')
			print('1. 입금')
			print('2. 출금')
			print('3. 조회')
			print('4. 종료')
			print('------------')
			option = int(input('메뉴 선택: '))

			if option == 4:
				print('프로그램을 종료합니다.')
				break
			elif option == 1:
				money = int(input('입금할 금액을 10000원 단위로 입력하세요: '))
				self.deposit(money)
			elif option == 2:
				money = int(input('출금할 금액을 10000원 단위로 입력하세요: '))
				self.withdraw(money)
			elif option == 3:
				self.print_balance()
			else:
				print('잘못된 메뉴 선택입니다. 다시 입력하세요.')

		

bank = BankAccount('KDT Bank')
bank.run()

# bank1 = BankAccount('KDT Bank')
# bank2 = BankAccount()