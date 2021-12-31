from tkinter import *
from tkinter import ttk
from bank_system import BankSystem

# forget previous frame loaded on tkinter window
def forget_previous_frame(window,form=None):
	_list = window.winfo_children()
	for item in _list:
		if item.winfo_children():
			_list.extend(item.winfo_children())
	
	for item in _list:
		if item.widgetName == "frame":
			item.pack_forget()

	if not form:
		Form = Frame(root, height=300)
		Form.pack(side=TOP, pady=20,padx=30)
		return Form

# update detail function
def update_details(user,fname,lname,house_no,street_no,city,pincode):
	first_name = fname.get()
	last_name = lname.get()
	if first_name:
		user.update_first_name(first_name)

	if last_name:
		user.update_last_name(last_name)

	address = [house_no.get(),street_no.get(),city.get(),pincode.get()]
	user.update_address(address)

	lbl_text.config(text="Details updated successfully",fg="green")

def update_user_details(user,admin_obj,customer=None):
	Form = forget_previous_frame(root)
	Form1 = Frame(root, height=300)
	Form1.pack(side=TOP)

	welcomeLabel = Label(Form, text ="Enter new details for {}".format(user) ,font=('Helvetica 12 bold', 12),fg="brown").grid(pady=10,row=1,column=1)

	global lbl_text
	lbl_text = Label(Form1, text ="",font=('Helvetica 13 bold', 13))
	lbl_text.pack()

	fnameLabel = Label(Form, text ="Enter new first name:").grid(row=3,column=0)
	fname = Entry(Form, textvariable="", font=(10))
	fname.grid(row=3,column=1)

	lnameLabel = Label(Form, text ="Enter new last name:").grid(row=4,column=0)
	lname = Entry(Form, textvariable="", font=(10))
	lname.grid(row=4,column=1)

	houseLabel = Label(Form, text ="Enter new House no.:").grid(row=5,column=0)
	house_no = Entry(Form, textvariable="", font=(10))
	house_no.grid(row=5,column=1)

	streetLabel = Label(Form, text ="Enter new Street no.:").grid(row=6,column=0)
	street_no = Entry(Form, textvariable="", font=(10))
	street_no.grid(row=6,column=1)

	cityLabel = Label(Form, text ="Enter new city:").grid(row=7,column=0)
	city = Entry(Form, textvariable="", font=(10))
	city.grid(row=7,column=1)

	pincodeLabel = Label(Form, text ="Enter new pincode:").grid(row=8,column=0)
	pincode = Entry(Form, textvariable="", font=(10))
	pincode.grid(row=8,column=1)

	
	if user == "Customer":
		Button(Form, text="Back", width=10, command=lambda:run_account_options(customer,admin_obj)).grid(pady=10,row=9,column=0)
		Button(Form, text="Submit", width=10, command=lambda:update_details(customer,fname,lname,house_no,street_no,city,pincode)).\
				grid(pady=10,row=9,column=1)
	else:
		Button(Form, text="Back", width=10, command=lambda:run_main_options(admin_obj)).grid(pady=10,row=9,column=0)
		Button(Form, text="Submit", width=10, command=lambda:update_details(admin_obj,fname,lname,house_no,street_no,city,pincode)).\
				grid(pady=10,row=9,column=1)


# customer profile settings
def run_account_options(customer,admin_obj):
	forget_previous_frame(root,True)
	Form1 = Frame(root, height=300)
	Form1.pack(side=TOP)
	Form = Frame(root, height=300)
	Form.pack(side=TOP, pady=20,padx=20)
	Form2 = Frame(root, height=300)
	Form2.pack(side=TOP)
	
	welcomeLabel = Label(Form1, text ="Welcome Admin to {} profile. Your Transaction Options Are: ".format(customer.get_first_name()) ,\
						font=('Helvetica 10 bold', 10),fg="brown").grid(row=1,column=1)

	def deposit_money(deposit_amount):
		amount = deposit_amount.get()
		if amount:
			amount = round(float(amount),2)
			customer.deposit(float(amount))
			lbl_text.config(text="{} deposited successfully.".format(amount),fg="green")


	def withdraw_money(withdraw_amount):
		amount = withdraw_amount.get()
		if amount:
			amount = round(float(amount),2)
			current_balance = customer.get_balance()
			if current_balance >= amount:
				customer.withdraw(amount)
				lbl_text.config(text="{} withdrawn successfully.".format(amount),fg="green")
			else:
				balance = abs(current_balance)+customer.overdraft_limit
				if balance >= amount:
					customer.withdraw(amount)
					lbl_text.config(text="{} withdrawn successfully.".format(amount),fg="green")
				else:
					lbl_text.config(text="Insufficient account balance",fg="red")


	def check_account_balance():
		balance = customer.get_balance()
		lbl_text.config(text="Account balance: {}".format(balance),fg="green")



	def view_customer_detail():
		Form = forget_previous_frame(root)

		fname = customer.get_first_name()
		lname = customer.get_last_name()
		address = customer.get_address()
		account_number = customer.get_account_no()
		current_balance = customer.get_balance()
		account_type = customer.get_account_type()
		interest_rate = customer.get_interest_rate()
		overdraft_limit = customer.get_overdraft_limit()

		Form1 = Frame(root, height=300)
		Form1.pack(side=TOP)

		Label(Form, text ="Customer details are as follows",font=('Helvetica 13 bold', 13),fg="brown").pack(pady=5)

		Label(Form1, text ="First name:",font=('Helvetica 11 bold', 11)).grid(pady=5,row=2,column=0)
		Label(Form1, text =fname,font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=2,column=1)

		Label(Form1, text ="Last name:",font=('Helvetica 11 bold', 11)).grid(pady=5,row=3,column=0)
		Label(Form1, text =lname,font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=3,column=1)

		Label(Form1, text ="Address:",font=('Helvetica 11 bold', 11)).grid(pady=5,row=4,column=0)
		Label(Form1, text =",".join(address[2:]),font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=4,column=1)
		Label(Form1, text =",".join(address[:2]),font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=5,column=1)

		Label(Form1, text ="Account number:",font=('Helvetica 11 bold', 11)).grid(pady=5,row=6,column=0)
		Label(Form1, text =account_number,font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=6,column=1)

		Label(Form1, text ="Current balance",font=('Helvetica 11 bold', 11)).grid(pady=5,row=7,column=0)
		Label(Form1, text =current_balance,font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=7,column=1)

		Label(Form1, text ="Account type",font=('Helvetica 11 bold', 11)).grid(pady=5,row=8,column=0)
		Label(Form1, text =account_type,font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=8,column=1)

		Label(Form1, text ="Interest rate",font=('Helvetica 11 bold', 11)).grid(pady=5,row=9,column=0)
		Label(Form1, text ="{}%".format(interest_rate),font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=9,column=1)

		Label(Form1, text ="Overdraft limit",font=('Helvetica 11 bold', 11)).grid(pady=5,row=10,column=0)
		Label(Form1, text =overdraft_limit,font=('Helvetica 13 bold', 11),fg="darkgreen").grid(pady=5,row=10,column=1)

		Button(Form, text="Back", width=10, command=lambda:run_account_options(customer,admin_obj)).pack(pady=10)



	global lbl_text
	lbl_text = Label(Form1, text ="",font=('Helvetica 13 bold', 13))
	lbl_text.grid(row=2,column=1)

	# deposit money form
	depositLabel = Label(Form, text ="Enter Amount:").grid(row=4,column=0)
	deposit_amount = Entry(Form, textvariable="", font=(10))
	deposit_amount.grid(row=4,column=1)
	deposit_button = Button(Form, text="Deposit money", width=12, command=lambda:deposit_money(deposit_amount))\
							.grid(row=4,column=3)


	# withdraw money form
	withdrawLabel = Label(Form, text ="Enter Amount:").grid(row=5,column=0)
	withdraw_amount = Entry(Form, textvariable="", font=(10))
	withdraw_amount.grid(row=5,column=1)
	withraw_button = Button(Form, text="Withdraw money", width=12, command=lambda:withdraw_money(withdraw_amount))\
							.grid(row=5,column=3)


	# check balance button
	Button(Form2, text="Check balance", width=20, command=check_account_balance).pack(padx=10, pady=10)

	# update customer details
	Button(Form2, text="Update name & address", width=20, command=lambda:update_user_details("Customer",admin_obj,customer)).pack(padx=10, pady=10)

	# print all customer details
	Button(Form2, text="Show customer detail", width=20, command=view_customer_detail).pack(padx=10, pady=10)

	# back to admin menu
	Button(Form2, text="Back", width=20, command=lambda:run_main_options(admin_obj)).pack(padx=10, pady=10)


def validate_customer(customer,admin_obj):
	customer_name = customer.get()
	found_customer = app.search_customers_by_name(customer_name)
	if found_customer:
		run_account_options(found_customer,admin_obj)
	else:
		lbl_text.config(text="The customer {} does not exist!\n Try again...".format(customer_name),fg="red")


def transfer_money(sender_name,sender_account,receiver_name,receiver_account,amount):
	sender_name = sender_name.get()
	sender_account = sender_account.get()
	receiver_name = receiver_name.get()
	receiver_account = receiver_account.get()
	amount = amount.get()

	if sender_name and sender_account and receiver_name and receiver_account and amount:
		sender_account = int(sender_account)
		receiver_account = int(receiver_account)
		amount = float(amount)
		sender,receiver = app.get_customer_by_account_number(sender_account,sender_name,receiver_account,receiver_name)
		if sender and receiver:
			msg = app.transferMoney(sender, receiver, amount)
			fg = "red"
			if not msg:
				msg = "{} transfered from {} account to\n{} account successfully.".format(amount,sender_name,receiver_name)
				fg = "green"
			lbl_text.config(text=msg,fg=fg)
		else:
			if not sender:
				msg = "Invalid sender details."
			elif not receiver:
				msg = "Invalid receiver details."

			lbl_text.config(text=msg,fg="red")
	else:
		lbl_text.config(text="Please fill following details",fg="red")


def delete_customer(customer_name,customer_account):
	customer_name = customer_name.get()
	customer_account = customer_account.get()

	if customer_name and customer_account:
		customer_account = int(customer_account)
		customer = app.verify_account_number_and_name(customer_account,customer_name)
		if customer:
			app.accounts_list.remove(customer)
			lbl_text.config(text="{} removed successfully".format(customer_name),fg="green")
		else:
			lbl_text.config(text="Invalid customer details",fg="red")
	else:
		lbl_text.config(text="Please fill following details",fg="red")


# admin menu dashboard
def run_main_options(admin_obj):
	Form = forget_previous_frame(root)	
	Form1 = Frame(root, height=300)
	Form1.pack(side=TOP)
	
	welcomeLabel = Label(Form, text ="Welcome Admin {} {}\n Avilable options are:".format(admin_obj.get_first_name(),admin_obj.get_last_name()) ,\
						font=('Helvetica 15 bold', 15),fg="brown").grid(row=1,column=1)

	lbl_text = Label(Form1, text ="",font=('Helvetica 10 bold', 10))
	lbl_text.pack(pady=5)

	def customer_search():
		Form = forget_previous_frame(root)
		lbl_username = Label(Form, text = "Enter Customer first name:", font=('arial', 10)).pack(padx=10, pady=10)
		customer = Entry(Form, textvariable="", font=(14))
		customer.pack(padx=10, pady=10)
		global lbl_text
		lbl_text = Label(Form, text='', font=('arial', 10))
		lbl_text.configure(font=("Helvetica 10 bold"))
		lbl_text.place(relx=0.6, rely=0.42, anchor='se')
		lbl_text.pack(padx=10, pady=10)
		Button(Form, text="Submit", width=10, command=lambda:validate_customer(customer,admin_obj)).pack(padx=10, pady=10)
		Button(Form, text="Back", width=10, command=lambda:run_main_options(admin_obj)).pack(padx=10, pady=10)

		
	def process_transfer():
		Form = forget_previous_frame(root)
		Form1 = Frame(root, height=300)
		Form1.pack(side=TOP)

		welcomeLabel = Label(Form, text ="Transfer Money",font=('Helvetica 12 bold', 12),fg="brown").grid(pady=10,row=1,column=1)

		global lbl_text
		lbl_text = Label(Form1, text ="",font=('Helvetica 13 bold', 13))
		lbl_text.pack()

		sendernameLabel = Label(Form, text ="Sender first name:").grid(row=3,column=0)
		sender_name = Entry(Form, textvariable="", font=(10))
		sender_name.grid(row=3,column=1)

		senderaccountLabel = Label(Form, text ="Sender account number:").grid(row=4,column=0)
		sender_account = Entry(Form, textvariable="", font=(10))
		sender_account.grid(row=4,column=1)

		amountLabel = Label(Form, text ="Amount to be transfered:").grid(row=5,column=0)
		amount = Entry(Form, textvariable="", font=(10))
		amount.grid(row=5,column=1)

		recieverLabel = Label(Form, text ="Receiver first name:").grid(row=6,column=0)
		receiver_name = Entry(Form, textvariable="", font=(10))
		receiver_name.grid(row=6,column=1)

		receiveraccountLabel = Label(Form, text ="Receiver account number:").grid(row=7,column=0)
		receiver_account = Entry(Form, textvariable="", font=(10))
		receiver_account.grid(row=7,column=1)

		Button(Form, text="Back", width=10, command=lambda:run_main_options(admin_obj)).grid(pady=10,row=9,column=0)
		Button(Form, text="Transfer", width=10, command=lambda:transfer_money(sender_name,sender_account,receiver_name,receiver_account,amount)).\
					grid(pady=10,row=9,column=1)


	def process_delete_customer():
		Form = forget_previous_frame(root)
		Form1 = Frame(root, height=300)
		Form1.pack(side=TOP)

		welcomeLabel = Label(Form, text ="Delete Customer",font=('Helvetica 12 bold', 12),fg="brown").grid(pady=10,row=1,column=1)

		global lbl_text
		lbl_text = Label(Form1, text ="",font=('Helvetica 13 bold', 13))
		lbl_text.pack()

		nameLabel = Label(Form, text ="Enter customer first name:").grid(row=3,column=0)
		customer_name = Entry(Form, textvariable="", font=(10))
		customer_name.grid(row=3,column=1)

		accountLabel = Label(Form, text ="Enter customer account number:").grid(pady=10,row=5,column=0)
		customer_account = Entry(Form, textvariable="", font=(10))
		customer_account.grid(pady=10,row=5,column=1)

		Button(Form, text="Back", width=10, command=lambda:run_main_options(admin_obj)).grid(pady=10,row=9,column=0)
		Button(Form, text="Delete customer", width=15, command=lambda:delete_customer(customer_name,customer_account)).\
					grid(pady=10,row=9,column=1)


	def view_all_customers(customers_list=None):
		Form = forget_previous_frame(root)
		Form1 = Frame(root, height=300)
		Form1.pack(side=TOP)
		canvas = Canvas(Form1)
		scrollbar = ttk.Scrollbar(Form1, orient="vertical", command=canvas.yview)
		scrollable_frame = ttk.Frame(canvas)

		scrollable_frame.bind(
			"<Configure>",
			lambda e: canvas.configure(
				scrollregion=canvas.bbox("all")
			)
		)

		canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
		canvas.configure(yscrollcommand=scrollbar.set)

		if not customers_list:
			customers_list = app.accounts_list
			Label(Form, text ="Customer details are as follows",font=('Helvetica 13 bold', 13),fg="brown").pack(pady=5)
		else:
			Label(Form, text ="Customers imported successfully\ndetails are as follows",font=('Helvetica 13 bold', 13),fg="brown").pack(pady=5)
			
		Button(Form, text="Back", width=10, command=lambda:run_main_options(admin_obj)).pack(pady=10)


		i = 1
		j = 1
		for customer in customers_list:
			fname = customer.get_first_name()
			lname = customer.get_last_name()
			address = customer.get_address()
			account_number = customer.get_account_no()
			current_balance = customer.get_balance()
			account_type = customer.get_account_type()
			interest_rate = customer.get_interest_rate()
			overdraft_limit = customer.get_overdraft_limit()

			ttk.Label(scrollable_frame, text ="Customer {}".format(i),font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)

			j+=1
			ttk.Label(scrollable_frame, text ="First name:",font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text =fname,font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)

			j+=1
			ttk.Label(scrollable_frame, text ="Last name:",font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text =lname,font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)

			j+=1
			ttk.Label(scrollable_frame, text ="Address:",font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text =",".join(address[2:]),font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)
			j+=1
			ttk.Label(scrollable_frame, text =",".join(address[:2]),font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)

			j+=1
			ttk.Label(scrollable_frame, text ="Account number:",font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text =account_number,font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)

			j+=1
			ttk.Label(scrollable_frame, text ="Current balance",font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text =current_balance,font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)

			j+=1
			ttk.Label(scrollable_frame, text ="Account type",font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text =account_type,font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)

			j+=1
			ttk.Label(scrollable_frame, text ="Interest rate",font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text ="{}%".format(interest_rate),font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)

			j+=1
			ttk.Label(scrollable_frame, text ="Overdraft limit",font=('Helvetica 11 bold', 11)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text =overdraft_limit,font=('Helvetica 13 bold', 11),foreground="darkgreen").grid(pady=5,row=j,column=1)

			j+=1
			ttk.Label(scrollable_frame, text ="-"*15,font=('Helvetica 13 bold', 13)).grid(pady=5,row=j,column=0)
			ttk.Label(scrollable_frame, text ="-"*15,font=('Helvetica 13 bold', 13)).grid(pady=5,row=j,column=1)
			j+=2
			i+=1

		Form1.pack()
		canvas.pack(side="left", expand=True)
		scrollbar.pack(side="right", fill="y")

	def process_customer_details():
		file = app.export_customer_details()
		lbl_text.config(text="Export customer detail successfully\n file saved as 'customer_details.csv'",fg="green")

	def process_generate_report():
		file,data = app.generate_report()

		Form = forget_previous_frame(root)
		Form1 = Frame(root, height=300)
		Form1.pack(side=TOP)

		lbl_text = Label(Form, text ="Management report genereted successfully\n file saved as 'management_report.csv'",font=('Helvetica 10 bold', 10),fg="green")
		lbl_text.pack(pady=10)
		
		i = 2
		for row in data:
			Label(Form1, text ="{}: {}".format(row[0],row[1])).grid(pady=5,row=i,column=0)
			i+=2

		Button(Form1, text="Back", width=10, command=lambda:run_main_options(admin_obj)).grid(pady=10,row=9,column=0)

	def process_import_file(path,lbl_text):
		path = path.get()
		if path:
			msg,added_customers = app.import_customer_details(path)
			if "Successfully" in msg:
				view_all_customers(added_customers)
			else:
				lbl_text.config(text=msg,fg="red")

				

	def process_import_customer_details():
		Form = forget_previous_frame(root)
		Form1 = Frame(root, height=300)
		Form1.pack(side=TOP)

		welcomeLabel = Label(Form, text ="Import customer details from file",font=('Helvetica 12 bold', 12),fg="brown").pack()

		lbl_text = Label(Form, text ="",font=('Helvetica 10 bold', 10))
		lbl_text.pack(pady=10)

		fileLabel = Label(Form1, text ="Enter file location:").grid(row=3,column=0)
		path = Entry(Form1, textvariable="", font=(10))
		path.grid(row=3,column=1)

		Button(Form1, text="Back", width=10, command=lambda:run_main_options(admin_obj)).grid(pady=10,row=9,column=0)
		Button(Form1, text="Import", width=15, command=lambda:process_import_file(path,lbl_text)).grid(pady=10,row=9,column=1)

	def add_new_customer(fname,lname,house_no,street_no,city,pincode,account_type,opening_balance,lbl_text):
		fname = fname.get()
		lname = lname.get()
		house_no = house_no.get()
		street_no = street_no.get()
		city = city.get()
		pincode = pincode.get()
		account_type = account_type.get()
		opening_balance = opening_balance.get()
		if fname and lname and house_no and street_no and city and pincode and account_type and opening_balance:
			opening_balance = round(float(opening_balance),2)
			account_type = account_type.capitalize()
			fname = fname.capitalize()
			lname = lname.capitalize()
			address = [house_no,street_no,city,pincode]
			customer_detail = [fname,lname,address,opening_balance,account_type]
			app.add_customer(customer_detail)
			lbl_text.config(text="{} added successfully".format(fname),fg = "green")
		else:
			lbl_text.config(text="Please fill following fields.",fg = "red")



	def process_add_customer():
		Form1 = forget_previous_frame(root)
		Form = Frame(root, height=300)
		Form.pack(side=TOP)

		welcomeLabel = Label(Form1, text ="Add new customer",font=('Helvetica 12 bold', 12),fg="brown").pack()

		lbl_text = Label(Form1, text ="",font=('Helvetica 10 bold', 10))
		lbl_text.pack(pady=5)

		fnameLabel = Label(Form, text ="Enter first name:").grid(pady=5,row=3,column=0)
		fname = Entry(Form, textvariable="", font=(10))
		fname.grid(pady=5,row=3,column=1)

		lnameLabel = Label(Form, text ="Enter last name:").grid(row=4,column=0)
		lname = Entry(Form, textvariable="", font=(10))
		lname.grid(row=4,column=1)

		lnameLabel = Label(Form, text ="Enter address details:").grid(row=5,column=0)
		houseLabel = Label(Form, text ="Enter House no.:").grid(row=6,column=0)
		house_no = Entry(Form, textvariable="", font=(10))
		house_no.grid(row=6,column=1)

		streetLabel = Label(Form, text ="Enter Street no.:").grid(row=7,column=0)
		street_no = Entry(Form, textvariable="", font=(10))
		street_no.grid(row=7,column=1)

		cityLabel = Label(Form, text ="Enter city:").grid(row=8,column=0)
		city = Entry(Form, textvariable="", font=(10))
		city.grid(row=8,column=1)

		pincodeLabel = Label(Form, text ="Enter pincode:").grid(row=9,column=0)
		pincode = Entry(Form, textvariable="", font=(10))
		pincode.grid(row=9,column=1)

		accounttypeLabel = Label(Form, text ="Enter account type\n(Saving,Current):").grid(row=10,column=0)
		account_type = Entry(Form, textvariable="", font=(10))
		account_type.grid(row=10,column=1)

		balanceLabel = Label(Form, text ="Enter opening balance:").grid(row=11,column=0)
		opening_balance = Entry(Form, textvariable="", font=(10))
		opening_balance.grid(row=11,column=1)

		Button(Form, text="Back", width=10, command=lambda:run_main_options(admin_obj)).grid(pady=10,row=12,column=0)
		Button(Form, text="Add", width=15, command=lambda:add_new_customer(fname,lname,house_no,street_no,city,pincode,\
						account_type,opening_balance,lbl_text)).grid(pady=10,row=12,column=1)
		

		
	# transfer money from one account to another
	Transfer_money = Button(Form, text="Transfer money", width=20, command=process_transfer)\
							.grid(pady=5, row=3, column=1)

	# search customer to perform operations
	search_customer_button = Button(Form, text="Customer search", width=20, command=customer_search)\
							.grid(pady=1, row=5, column=1)

	# remove customer account
	remove_customer_button = Button(Form, text="Delete customer", width=20, command=process_delete_customer)\
							.grid(pady=1, row=7, column=1)

	# view all customer details
	view_customers_button = Button(Form, text="Show all customer details", width=20, command=view_all_customers)\
							.grid(pady=1, row=9, column=1)

	# update admin own details
	update_admin_button = Button(Form, text="Update own(Admin) Details", width=20, command=lambda:update_user_details("Admin",admin_obj))\
							.grid(pady=1, row=11, column=1)
	
	# export customer details
	export_customer_button = Button(Form, text="Export customer details", width=20, command=process_customer_details)\
							.grid(pady=1, row=13, column=1)

	# import customer details
	import_customer_button = Button(Form, text="Import customer details", width=20, command=process_import_customer_details)\
							.grid(pady=1, row=15, column=1)

	# add new customer
	add_customer_button = Button(Form, text="Add customer", width=20, command=process_add_customer)\
							.grid(pady=1, row=17, column=1)

	# generate management report
	generate_report_button = Button(Form, text="Generate management\nreport", width=20, command=process_generate_report)\
							.grid(pady=1, row=18, column=1)



# STEP A.2
def validate_login():
	username = USERNAME.get()
	password = PASSWORD.get()
	if username and password:
		msg,admin_obj= app.admin_login(username,password)
		if admin_obj != None and 'successful' in msg:
			run_main_options(admin_obj)
		else:
			lbl_text.config(text=msg,fg="red")
	else:
		lbl_text.config(text="Please complete the required field!", fg="red")


if __name__=="__main__":
	app = BankSystem()

	# admin login form : STEP A.1
	root = Tk()  
	root.geometry('600x550')  
	root.title('Bank Management System')
	root.resizable(0, 0)

	Top = Frame(root, bd=2,  relief=RIDGE)
	Top.pack(side=TOP, fill=X)
	Form = Frame(root, height=300)
	Form.pack(side=TOP, pady=20)

	USERNAME = StringVar()
	PASSWORD = StringVar()

	lbl_title = Label(Top, text = "Enter login details", font=('arial', 15))
	lbl_title.pack(fill=X)
	lbl_username = Label(Form, text = "Username:", font=('arial', 14), bd=15)
	lbl_username.configure(font=(" Helvetica 15 bold"),fg="thistle4")
	lbl_username.grid(row=0, sticky="e")
	lbl_password = Label(Form, text = "Password:", font=('arial', 14), bd=15)
	lbl_password.configure(font=(" Helvetica 15 bold"),fg="thistle4")
	lbl_password.grid(row=1, sticky="e")
	lbl_text = Label(Form)
	lbl_text.grid(row=2, columnspan=2)

	username = Entry(Form, textvariable=USERNAME, font=(14))
	username.grid(row=0, column=1)
	password = Entry(Form, textvariable=PASSWORD, show="*", font=(14))
	password.grid(row=1, column=1)

	btn_login = Button(Form, text="Login", width=20, command=validate_login).grid(pady=1, row=3, columnspan=2)
	root.mainloop()
