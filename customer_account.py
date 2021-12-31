
class CustomerAccount:
	def __init__(self, fname, lname, address, account_no, balance, account_type):
		interest_rate_list = {"Saving":5,"Current":7}
		self.fname = fname
		self.lname = lname
		self.address = address
		self.account_no = account_no
		self.balance = float(balance)
		self.account_type = account_type
		self.interest_rate = interest_rate_list.get(account_type,0)
		if account_type == "Current":
			self.overdraft_limit = float(balance*3/100)
		else:
			self.overdraft_limit = 0


	def update_first_name(self, fname):
		self.fname = fname

	def update_last_name(self, lname):
		self.lname = lname

	def get_first_name(self):
		return self.fname

	def get_last_name(self):
		return self.lname

	def update_address(self, addr):
		self.address = addr

	def get_address(self):
		return self.address

	def deposit(self, amount):
		self.balance+=amount
		

	def withdraw(self, amount):
		self.balance-=amount
		

	def print_balance(self):
		print("\n The account balance is %.2f" %self.balance)

	def get_balance(self):
		return self.balance

	def get_interest_rate(self):
		return self.interest_rate

	def get_account_no(self):
		return self.account_no

	def get_account_type(self):
		return self.account_type

	def get_overdraft_limit(self):
		return self.overdraft_limit

	def account_menu(self):
		print ("\n Your Transaction Options Are:")
		print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print ("1) Deposit money")
		print ("2) Withdraw money")
		print ("3) Check balance")
		print ("4) Update customer name & address")
		print ("5) Show customer details")
		print ("6) Back")
		print (" ")
		option = int(input ("Choose your option: "))
		return option

	def print_details(self):
		#STEP A.4.3
		 print("First name: %s" %self.fname)
		 print("Last name: %s" %self.lname)
		 print("Account No: %s" %self.account_no)
		 print("Address: %s" %self.address[0])
		 print("         %s" %self.address[1])
		 print("         %s" %self.address[2])
		 print("         %s" %self.address[3])
		 print("Account Type: %s" %self.account_type)
		 print("Interest rate: {}%".format(self.interest_rate))
		 print("Overdraft Limit: %s" %self.overdraft_limit)
		 print(" ")

	def fetch_customer_detail(self):
		customer_detail = [self.fname,self.lname,", ".join(self.address),self.account_no,self.balance,self.account_type,\
							self.interest_rate,self.overdraft_limit]
		return customer_detail

	def process_withdraw(self,amount):
		self.withdraw(amount)
		print("\n {} successfully withdraw from the account".format(amount))
		self.print_balance()

	def run_account_options(self):
		loop = 1
		while loop == 1:
			choice = self.account_menu()
			if choice == 1:
				amount = float(input("\n Please enter amount to be deposited: "))
				self.deposit(amount)
				print("\n {} successfully deposited to the account".format(amount))
				self.print_balance()
			elif choice == 2:
				amount = float(input("\n Please enter amount to be withdrawn: "))
				if self.balance >= amount:
					self.process_withdraw(amount)
				else:
					balance = abs(self.balance)+self.overdraft_limit
					if balance>=amount:
						self.process_withdraw(amount)
					else:
						if self.overdraft_limit>0:
							print("\nOverdraft limit execeeded.")
						else:
							print("\nInsufficient balance.")

			elif choice == 3:
				#STEP A.4.4
				self.print_balance()
			elif choice == 4:
				#STEP A.4.2
				fname = input("\n Enter new customer first name: ")
				if fname:
					self.update_first_name(fname)

				sname = input("\n Enter new customer last name: ")
				if sname:
					self.update_last_name(sname)
				
				address = [input("\n House No.: "),input("\n Street: "),input("\n City: "),input("\n Postcode: ")]
				self.update_address(address)
				print("\n Customer details updated successfully.")

			elif choice == 5:
				self.print_details()
			elif choice == 6:
				loop = 0
		print ("\n Exit account operations")
