import sqlite3
conn = sqlite3.connect("loans.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Loans
             (id INTEGER PRIMARY KEY, 
             amount REAL NOT NULL, 
             duration INTEGER NOT NULL,
             interestRate REAL NOT NULL,
             paymentStart INTEGER NOT NULL,
             accruementStart INTEGER NOT NULL,
             isCompound INTEGER NOT NULL)''')

def print_main_menu():
  print("What would you like to do?")
  print("1. Add a loan")
  print("2. View loans")
  print("3. Update a loan")
  print("4. Delete a loan")
  print("5. Calculate")
  print("6. What should I ask my loan officer?")
  print("7. Exit")

def add_loan():
  loan_amount = int(input("\nHow much is the loan:  "))
  loan_duration = int(input("How long is the loan (in months):  "))
  loan_interest_rate = float(input("What is the interest rate on the loan:  ")) / 100
  payment_start = int(input("In how many months do you start to pay off the loan?  "))
  accruement_start = int(input("In how many months does the loan start to accrue interest?  "))
  is_compound = int(input("Does your loan use compounded interest (0 for no, 1 for yes)?  "))

  c.execute('''INSERT INTO Loans ('amount', 'duration', 'interestRate', 'paymentStart', 'accruementStart', 'isCompound') VALUES (?,?,?,?,?,?)''', 
            (loan_amount, loan_duration, loan_interest_rate, payment_start, accruement_start, is_compound))
  conn.commit()
  print("Loan added!\n")

def view_loans():
  fetched_loans = c.execute("SELECT id, amount, duration, interestRate, paymentStart, accruementStart, isCompound FROM Loans")
  print("\nLoans:")
  for loan in fetched_loans:
    print(f"id: {loan[0]}, amount: ${round(loan[1], 2):,.2f}, duration: {loan[2]} months, interest rate: {loan[3] * 100}%, start payment in: {loan[4]} months, starts accruing interest in: {loan[5]} months, uses compound interest: {'false' if loan[6] == 0 else 'true'}")
  print()

def update_loan():
  view_loans()
  loan_id = input("What is the id of the loan you want to update?  ")
  fetched_loan = c.execute("SELECT amount, duration, interestRate, paymentStart, accruementStart, isCompound FROM Loans WHERE id=?", (loan_id)).fetchone()
  print("\nPress enter to skip and keep the current value")
  loan_amount = input("How much is the loan:  ")
  loan_amount = fetched_loan[0] if loan_amount == '' else int(loan_amount) 
  loan_duration = input("How long is the loan (in months):  ")
  loan_duration = fetched_loan[1] if loan_duration == '' else int(loan_duration)
  loan_interest_rate = input("What is the interest rate on the loan:  ")
  loan_interest_rate = fetched_loan[2] if loan_interest_rate == '' else float(loan_interest_rate) / 100
  payment_start = input("In how many months do you start to pay off the loan?  ")
  payment_start = fetched_loan[3] if payment_start == '' else int(payment_start)
  accruement_start = input("In how many months does the loan start to accrue interest?  ")
  accruement_start = fetched_loan[4] if accruement_start == '' else int(accruement_start)
  is_compound = input("Does your loan use compounded interest (0 for no, 1 for yes)?  ")
  is_compound = fetched_loan[5] if is_compound == '' else int(is_compound)

  c.execute("UPDATE Loans SET amount=?,duration=?,interestRate=?,paymentStart=?,accruementStart=?,isCompound=? WHERE id=?", 
            (loan_amount, loan_duration, loan_interest_rate, payment_start, accruement_start, is_compound, loan_id))
  conn.commit()
  print("Loan Updated!\n")

def delete_loan():
  view_loans();
  loan_id = input("What is the id of the loan you want to delete?  ")
  c.execute('''DELETE FROM Loans WHERE id=?''', (loan_id))
  conn.commit()
  print("Loan Deleted!\n")

def get_compound_interest_principal(principal, rate, number_of_compounds_per_interval, intervals):
  return principal * (1 + (rate / number_of_compounds_per_interval)) ** (number_of_compounds_per_interval * intervals)

def get_simple_interest_principal(principal, rate, intervals):
  return principal + (principal * rate * intervals)

def calculate_loans():
  loans = c.execute("SELECT id, amount, duration, interestRate, paymentStart, accruementStart, isCompound FROM Loans")
  print("\nCalculating loans. . .")
  total = 0
  avg_payments = []
  for loan in loans:

    payments = []

    (loan_id, loan_amount, loan_length, interest_rate, payment_start, accruement_start, is_compound) = loan
    days_per_month = 30
    payment_free_days = payment_start * days_per_month
    payment_days = (loan_length - payment_start) * days_per_month
    interest_free_days = accruement_start * days_per_month
    interest_days = (loan_length - accruement_start) * days_per_month
    loan_days = loan_length * days_per_month
    principal = loan_amount
    daily_interest_rate = interest_rate / 365
    loan_total = 0

    if is_compound == 0:
      original_principal = principal
      for i in range(0, loan_days):
        days_left = loan_days - i
        if i >= payment_free_days: # if past payment start date, pay on the first of every month
          if i % days_per_month < 1:
            payment = get_simple_interest_principal(principal, daily_interest_rate, days_left) / (days_left // days_per_month)
            principal -= payment
            loan_total += payment
            payments.append(payment)
        if i >= interest_free_days: # if past interest start date, add compound interest
          principal += original_principal * daily_interest_rate
    elif is_compound == 1:
      for i in range(0, loan_days):
        days_left = loan_days - i
        if i >= payment_free_days: # if past payment start date, pay on the first of every month
          if i % days_per_month < 1:
            payment = get_compound_interest_principal(principal, daily_interest_rate, 1, days_left) / (days_left // days_per_month)
            principal -= payment
            loan_total += payment
            payments.append(payment)
        if i >= interest_free_days: # if past interest start date, add simple interest
          principal += principal * daily_interest_rate
      
      avg_payment = round(sum(payments) / len(payments), 2)
      avg_payments.append(avg_payment)

      print(f"Loan {loan_id} total: ${round(loan_total, 2):,.2f}")
      print(f"\tAverage monthly payment: ${avg_payment:,.2f}")
      total += loan_total
    elif is_compound == 1:
      monthly_interest_rate = interest_rate / 12
      loan_total = loan_amount * (1 + (monthly_interest_rate / days_per_month)) ** (days_per_month * non_payment_length)
      print(f"Loan {loan_id} total: ${round(loan_total, 2):,.2f}")
      total += loan_total
        
  print(f"\nTotal of all loans: ${round(total, 2):,}")
  print(f"\tTotal average monthly payment: ${round(sum(avg_payments), 2):,.2f}\n")


def close_app():
  global should_exit
  conn.close()
  should_exit = True

should_exit = False
  
def main():

  while not should_exit:
    print_main_menu()
    main_menu_selection = int(input())

    if main_menu_selection == 1:
      add_loan()
    elif main_menu_selection == 2:
      view_loans()
    elif main_menu_selection == 3:
      update_loan()
    elif main_menu_selection == 4:
      delete_loan()
    elif main_menu_selection == 5:
      calculate_loans()
    elif main_menu_selection == 6:
      print("\nrecommended questions coming soon\n")
    elif main_menu_selection == 7:
      close_app()

if __name__ == "__main__":
  main()