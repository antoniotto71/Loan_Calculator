import math
import argparse
import sys

parser = argparse.ArgumentParser("Loan Calculator")

parser.add_argument("--type", type=str, help="Enter the type of loan annuity or diff")
parser.add_argument("--payment", type=float, help="Enter the monthly payment")
parser.add_argument("--principal", type=int, help="Enter the loan principal")
parser.add_argument("--periods", type=int, help="Enter the number of months")
parser.add_argument("--interest", type=float, help="Enter the interest without percent sign")

args = parser.parse_args()

if args.interest is not None:
    nominal_interest = args.interest / 1200
else:
    nominal_interest = 0


def interest_factor(nominal, number):
    return ((1 + nominal) ** number - 1) / (nominal * (1 + nominal) ** number)


def principal(monthly_payment, nominal, number):
    return monthly_payment * interest_factor(nominal, number)


def payment(principal_payment, nominal, number):
    return principal_payment / interest_factor(nominal, number)


def differentiated_payment(principal_payment, nominal, number, month):
    return principal_payment / number + nominal * (
                principal_payment - (principal_payment * (month - 1) / number))


def fault():
    print("Incorrect parameters")
    sys.exit()


def check_negative(par1, par2, par3):
    if par1 < 0 or par2 < 0 or par3 < 0:
        fault()


if args.type is None:
    fault()

if args.type != "annuity":
    if args.type != "diff":
        fault()

if args.type == "diff" and args.payment is not None:
    fault()
if args.interest is None:
    fault()
if len(vars(args)) < 4:
    fault()

if args.type == "diff" and args.payment is None:
    check_negative(args.principal, nominal_interest, args.periods)
    total = 0
    for current_month in range(1, args.periods + 1):
        diff_payment = math.ceil(differentiated_payment(args.principal, nominal_interest, args.periods, current_month))
        total += diff_payment
        print(f"Month {current_month}: payment is {diff_payment}")
    overpayment = total - args.principal
    print()
    print("Overpayment = " + f"{overpayment}")

if args.type == 'annuity':
    if args.periods is None:
        check_negative(args.payment, nominal_interest, args.principal)
        periods = math.log(args.payment / (args.payment - nominal_interest * args.principal), 1 + nominal_interest)
        periods = math.ceil(periods)
        overpayment = int(periods * args.payment - args.principal)
        if periods % 12 == 0:
            plural = "" if periods == 12 else "s"
            print(f"It will take {periods // 12} year{plural}" + " to repay this loan!")
        elif periods < 11:
            plural_month = "s" if periods > 1 else ""
            print(f"It will take {periods} month{plural_month} to repay this loan!")
        elif periods > 12:
            plural = "" if periods // 12 == 1 else "s"
            plural_month = "" if periods % 12 == 1 else "s"
            print(f"It will take {periods // 12} year{plural} and {periods % 12} month{plural_month} to repay this loan!")
        print("Overpayment = " + f"{overpayment}")
    elif args.principal is None:
        check_negative(args.payment, nominal_interest, args.periods)
        principal = int(principal(args.payment, nominal_interest, args.periods))
        overpayment = int(args.payment * args.periods - principal)
        print("Your loan principal = " + str(principal) + "!")
        print("Overpayment = " + f"{overpayment}")
    elif args.payment is None:
        check_negative(args.principal, nominal_interest, args.periods)
        payment = math.ceil(payment(args.principal, nominal_interest, args.periods))
        overpayment = int(payment * args.periods - args.principal)
        print("Your monthly payment = " + str(payment) + "!")
        print("Overpayment = " + f"{overpayment}")

