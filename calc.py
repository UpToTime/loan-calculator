
def calc_loan(loans):
  print("Calculating loans. . .")
  total = 0
  for loan in loans:
    interest = 0
    loan_amount = loan[0]
    loan_length = loan[1]
    interest_rate = loan[2]
    daily_interest_rate = interest_rate / 365
    daily_interest = daily_interest_rate * loan_amount
    monthly_interest = daily_interest * 30
    total_interest = monthly_interest * loan_length
    total_loan_after_grad = total_interest + loan_amount
    total += total_loan_after_grad
  return total


# spr_2020_total = calc_loan([(10000, 12, 5 / 100)]);
# sum_2020_total = calc_loan(4.21, 1250, 12);
# fall_2020_total = calc_loan(4.21, 2500, 9);
# spr_2021_total = calc_loan(4.21, 2500, 5);

# print(spr_2020_total + sum_2020_total + fall_2020_total + spr_2021_total)

def print_main_menu():
  print("What would you like to do?")
  print("1. Add a loan")
  print("2. Calculate")
  print("3. Exit")

loans = []

should_exit = False
while not should_exit:
  print_main_menu()
  main_menu_selection = int(input())
  if main_menu_selection == 1:
    loan_amount = int(input("How much is the loan:\t"))
    loan_duration = int(input("How long is the loan:\t"))
    loan_interest_rate = float(input("What is the interest rate on the loan:\t"))
    loan_interest_rate /= 100
    loans.append((loan_amount, loan_duration, loan_interest_rate))
  elif main_menu_selection == 2:
    print()
    print(calc_loan(loans))
    print()
  elif main_menu_selection == 3:
    should_exit = True