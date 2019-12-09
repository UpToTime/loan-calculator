import sqlite3
conn = sqlite3.connect("loans.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS Loans
             (id INTEGER PRIMARY KEY, 
             amount REAL NOT NULL, 
             duration INTEGER NOT NULL,
             interestRate REAL NOT NULL)''')

def print_main_menu():
  print("What would you like to do?")
  print("1. Add a loan")
  print("2. View loans")
  print("3. Update a loan")
  print("4. Delete a loan")
  print("5. Calculate")
  print("6. Exit")

def add_loan():
  loan_amount = int(input("\nHow much is the loan:  "))
  loan_duration = int(input("How long is the loan (in months):  "))
  loan_interest_rate = float(input("What is the interest rate on the loan:  ")) / 100

  c.execute('''INSERT INTO Loans ('amount', 'duration', 'interestRate') VALUES (?,?,?)''', (loan_amount, loan_duration, loan_interest_rate))
  conn.commit()
  print("Loan added!\n")

def view_loans():
  fetched_loans = c.execute("SELECT id, amount, duration, interestRate FROM Loans")
  print("\nLoans:")
  for loan in fetched_loans:
    print(f"id: {loan[0]}, amount: ${round(loan[1], 2):,}, duration: {loan[2]} months, interest rate: {loan[3] * 100}%")
  print()

def update_loan():
  view_loans()
  loan_id = input("What is the id of the loan you want to update?  ")
  fetched_loan = c.execute("SELECT amount, duration, interestRate FROM Loans WHERE id=?", (loan_id)).fetchone()
  print("\nPress enter to skip and keep the current value")
  loan_amount = input("How much is the loan:  ")
  loan_amount = fetched_loan[0] if loan_amount == '' else int(loan_amount) 
  loan_duration = input("How long is the loan (in months):  ")
  loan_duration = fetched_loan[1] if loan_duration == '' else int(loan_duration)
  loan_interest_rate = input("What is the interest rate on the loan:  ")
  loan_interest_rate = fetched_loan[2] if loan_interest_rate == '' else float(loan_interest_rate) / 100

  c.execute("UPDATE Loans SET amount=?,duration=?,interestRate=? WHERE id=?", (loan_amount, loan_duration, loan_interest_rate, loan_id))
  conn.commit()
  print("Loan Updated!\n")

def delete_loan():
  view_loans();
  loan_id = input("What is the id of the loan you want to delete?  ")
  c.execute('''DELETE FROM Loans WHERE id=?''', (loan_id))
  conn.commit()
  print("Loan Deleted!\n")

def calculate_loans():
  loans = c.execute("SELECT id, amount, duration, interestRate FROM Loans")
  print("\nCalculating loans. . .")
  total = 0
  for loan in loans:
    interest = 0
    loan_id = loan[0]
    loan_amount = loan[1]
    loan_length = loan[2]
    interest_rate = loan[3]
    daily_interest_rate = interest_rate / 365
    daily_interest = daily_interest_rate * loan_amount
    monthly_interest = daily_interest * 30
    total_interest = monthly_interest * loan_length
    total_loan_after_grad = total_interest + loan_amount
    total += total_loan_after_grad
    print(f"Loan {loan_id} total: ${round(total_loan_after_grad, 2):,}")
  print(f"\nTotal of all loans: ${round(total, 2):,}\n")

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
      close_app()

if __name__ == "__main__":
  main()