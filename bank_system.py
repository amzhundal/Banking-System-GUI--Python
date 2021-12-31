import os,csv,sys

from customer_account import CustomerAccount
from admin import Admin

accounts_list = []
admins_list = []

class BankSystem(object):
	def __init__(self):
		self.accounts_list = []
		self.admins_list = []
		self.account_no = 1234
		self.load_bank_data()

	def add_customer(self,customer_detail):
		self.account_no += 1
		customer = CustomerAccount(customer_detail[0], customer_detail[1], customer_detail[2], self.account_no, customer_detail[3], customer_detail[4].capitalize())
		self.accounts_list.append(customer)
		return customer

	def load_bank_data(self):

		# create customers
		customer_1 = CustomerAccount("Adam", "Smith", ["14", "Wilcot Street", "Bath", "B5 5RT"], self.account_no, 5000.00,"Saving")
		self.accounts_list.append(customer_1)

		self.account_no+=1
		customer_2 = CustomerAccount("David", "White", ["60", "Holborn Viaduct", "London", "EC1A 2FD"], self.account_no, 3200.00, "Current")
		self.accounts_list.append(customer_2)

		self.account_no+=1
		customer_3 = CustomerAccount("Alice", "Churchil", ["5", "Cardigan Street", "Birmingham", "B4 7BD"], self.account_no, 18000.00, "Current")
		self.accounts_list.append(customer_3)

		self.account_no+=1
		customer_4 = CustomerAccount("Ali", "Abdallah",["44", "Churchill Way West", "Basingstoke", "RG21 6YR"], self.account_no, 40.00, "Saving")
		self.accounts_list.append(customer_4)

		# create admins
		admin_1 = Admin("Julian", "Padget", ["12", "London Road", "Birmingham", "B95 7TT"], "id1188", "1441", True)
		self.admins_list.append(admin_1)

		admin_2 = Admin("Cathy",  "Newman", ["47", "Mars Street", "Newcastle", "NE12 6TZ"], "id3313", "2442", False)
		self.admins_list.append(admin_2)

	def export_customer_details(self):
		file_path = os.path.join(sys.path[0],"customer_details.csv")
		with open(file_path, "w") as csv_file:
			writer = csv.writer(csv_file, delimiter=',')
			writer.writerow(['first name','last name','address','account number','balance','account type','interest rate(%)','overdraft limit'])
			for account in self.accounts_list:
				detail = account.fetch_customer_detail()
				writer.writerow(detail)
		return file_path
		


	def import_customer_details(self,file_path):
		new_added_customers = []
		if file_path.endswith(".csv"):
			if os.path.exists(file_path):
				with open(file_path,'r')as f:
					data = csv.reader(f)
					initial = True
					for row in data:
						if initial:
							initial = False
							continue
						row[2] = row[2].split(",")
						customer = self.add_customer(row)
						customer.print_details()
						new_added_customers.append(customer)
				print("\n Successfully imported customer details.")
				message = "Successfully imported customer details."
			else:
				print("\n File doesn't exists")
				message = "File doesn't exists"
		else:
			print("\n Please provide '.csv' file")
			message = "Please provide '.csv' file"
		
		return message,new_added_customers


	def search_admins_by_name(self, admin_username):
		#STEP A.2
		found_admin = None
		for a in self.admins_list:
			username = a.get_username()
			if username == admin_username:
				found_admin = a
				break
		
		return found_admin


	def search_customers_by_name(self, customer_lname):
		found_customer = None
		for a in self.accounts_list:
			lname = a.get_first_name()
			if lname == customer_lname:
				found_customer = a
				break
		if found_customer == None:
			print("\n The customer %s does not exist! Try again...\n" %customer_lname)

		return found_customer
			

	def main_menu(self):
		#print the options you have
		print()
		print()
		print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print ("Welcome to the Python Bank System")
		print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		print ("1) Admin login")
		print ("2) Quit Python Bank System")
		print (" ")
		option = int(input ("Choose your option: "))
		return option


	def run_main_options(self):
		loop = 1
		while loop == 1:
			choice = self.main_menu()
			if choice == 1:
				username = input ("\n Please input admin username: ")
				password = input ("\n Please input admin password: ")
				msg, admin_obj = self.admin_login(username, password)
				print(msg)
				if admin_obj != None and 'successful' in msg:
					self.run_admin_options(admin_obj)
			elif choice == 2:
				loop = 0
		print ("\n Thank-You for stopping by the bank!")


	def verify_account_number_and_name(self,account_number,fname):
		for customer in self.accounts_list:
			account_num = customer.get_account_no()
			name = customer.get_first_name()
			if account_number == account_num and name == fname :
				return customer


	def get_customer_by_account_number(self,sender_account_number,sender_name,receiver_account_number, receiver_name):
		sender = self.verify_account_number_and_name(sender_account_number,sender_name)
		reciever = self.verify_account_number_and_name(receiver_account_number,receiver_name)
		return sender,reciever

	def transferMoney(self, sender, reciever, amount):
		current_balance = sender.get_balance()
		if current_balance>amount:
			sender.withdraw(amount)
			reciever.deposit(amount)
			print("\nTransfered money successfully.")
		else:
			print("\nInsufficient amount.")
			message = "Insufficient account balance"
			return message

	def admin_login(self, username, password):
		# STEP A.1
		found_admin = self.search_admins_by_name(username)
		if found_admin != None:
			if found_admin.get_password() == password:
				msg = "Login successful"
			else:
				msg = "Password is incorrect."
		else:
			msg = "The Admin {} does not exist! Try again...".format(username)
		return msg, found_admin

	def admin_menu(self, admin_obj):
		#print the options you have
		 print (" ")
		 print ("Welcome Admin %s %s : Avilable options are:" %(admin_obj.get_first_name(), admin_obj.get_last_name()))
		 print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
		 print ("1) Transfer money")
		 print ("2) Search customer account for operations & profile settings")
		 print ("3) Delete customer")
		 print ("4) Print all customers detail")
		 # print ("5) Search for customer")
		 print ("5) Update Admin name & address")
		 print ("6) Export customer details")
		 print ("7) Import customer details")
		 print ("8) Add new customer")
		 print ("9) Generate management report")
		 # print ("10) Sign out")
		 print (" ")
		 option = int(input ("Choose your option: "))
		 return option


	def run_admin_options(self, admin_obj):
		loop = 1
		while loop == 1:
			choice = self.admin_menu(admin_obj)
			if choice == 1:
				sender_name = input("\n Please input sender name: ").capitalize()
				sender_account_number = int(input("\n Please input sender account number: "))
				amount = float(input("\n Please input the amount to be transferred: "))
				receiver_name = input("\n Please input reciever name: ").capitalize()
				receiver_account_number = int(input("\n Please input receiver account number: "))
				sender,reciever = self.get_customer_by_account_number(sender_account_number,sender_name,receiver_account_number,receiver_name)
				if sender and reciever:
					self.transferMoney(sender, reciever, amount)

				else:
					if not sender:
						print("Invalid sender details.")
					elif not reciever:
						print("Invalid reciever details.")
			elif choice == 2:
				#STEP A.4
				customer_name = input("\n Please input customer first name: ").capitalize()
				customer_account = self.search_customers_by_name(customer_name)
				if customer_account != None:
					customer_account.run_account_options()

			elif choice == 3:
				#STEP A.5
				 customer_name = input("\n input customer first name you want to delete: ").capitalize()
				 customer_account = self.search_customers_by_name(customer_name)
				 if customer_account != None:
					 self.accounts_list.remove(customer_account)
					 print("%s was deleted successfully!" %customer_name)

			elif choice == 4:
				#STEP A.6
				 self.print_all_accounts_details()

			# elif choice == 5:
			# 	customer_name = input("\n input customer name you want to search: ")
			# 	customer_account = self.search_customers_by_name(customer_name)
			# 	if customer_account != None:
			# 		print("\n Customer found")
			# 		customer_account.print_details()

			elif choice == 5:
				fname = input("\n Enter new first name: ")
				sname = input("\n Enter new last name: ")
				if fname:
					admin_obj.update_first_name(fname)
				if sname:
					admin_obj.update_last_name(sname)

				address = [input("\n Enter House no: "),input("\n Enter Street no: "),input("\n Enter City: "),\
									input("\n Enter Postcode: ")]
				admin_obj.update_address(address)
				print("\nAdmin details updated successfully")

			elif choice == 6:
				file_path = self.export_customer_details()
				print("\n Export Customer details at location: {}".format(file_path))

			elif choice == 7:
				path = input("\n Enter file path: ")
				self.import_customer_details(path)

			elif choice == 8:
				print("Enter customer detail ")
				customer_detail = [input("Enter first name: ").capitalize(),input("Enter last name: ").capitalize(),[ \
									input("Enter House no: "),input("Enter Street no: "),input("Enter City: "),\
									input("Enter Pincode: ")],float(input("Enter opening balance: ")),input("Enter Account Type(Saving,Current): ").capitalize()]

				self.add_customer(customer_detail)
				print("\n Customer added successfully.")

			elif choice == 9:
				file_path,data = self.generate_report()
				print("\nReport generated successfully at {}".format(file_path))

		print ("\n Exit account operations")

	def generate_report(self):
		details = self.get_report_details()
		description = ["Total Number Of Customers","Sum Of All Accounts Balance",\
						"Sum of Interest Rate of all accounts","Sum of Overdraft limits taken by customers"]
		data = zip(description,details)
		file = "management_report.csv"
		file_path = os.path.join(sys.path[0],file)
		with open(file_path, "w") as csv_file:
			writer = csv.writer(csv_file, delimiter=',')
			for row in data:
				writer.writerow(row)
				print("\n{} : {}".format(row[0],row[1]))
		return file_path,zip(description,details)
		


	def get_report_details(self):
		total_customers = len(self.accounts_list)
		bank_account_balance_sum = overdraft_sum = interest_rate_sum = 0
		for account in self.accounts_list:
			balance = account.get_balance()
			bank_account_balance_sum += balance
			if balance > 0:
				interest_rate_sum += balance * account.get_interest_rate()/100
			else:
				overdraft_sum += abs(balance)

		return [total_customers,bank_account_balance_sum,interest_rate_sum,overdraft_sum]


	def print_all_accounts_details(self):
			# list related operation - move to main.py
			i = 0
			for c in self.accounts_list:
				i+=1
				print('\n %d. ' %i, end = ' ')
				c.print_details()
				print("------------------------")



if __name__=="__main__":
	app = BankSystem()
	app.run_main_options()