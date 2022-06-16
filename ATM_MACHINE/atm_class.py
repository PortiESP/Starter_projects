import os, time, platform
from random import randint
from os import system, path, getcwd
from datetime import datetime

class ATM:

    def __init__(self):

        self.balance = 0
        self.username = None
        self.accountID = self.generateId()

        self.menuOptions = ["Deposit money", "Withdraw money", "Make transaction", "View logs", "Update data", "Exit"]
        self.logs = []
        self.active = True

        self.loadLogs()

        self.newLog("[@] Login to ATM")




    # ATM operation: deposit
    def deposit(self, amount):
        self.balance += amount
        self.newLog(f"[+] Operation success, deposited founds ${amount}")

    # ATM operation: withdrawal
    def withdraw(self, amount):
        if self.balance - amount >= 0:
            self.balance -= amount
            self.newLog(f"[-] Operation success, retired founds ${amount}")
        else:
            self.newLog(f"[!] Operation failed, insuficiente founds")

    # ATM operation: make transaction
    def makeTransaction(self, dest, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.newLog(f"[-] Transaction success, {amount} sent to {dest}")
        else:
            self.newLog(f"[!] Transaction failed, insuficient founds")

    # ATM operation: view logs
    def printLogs(self):
        print("\n")
        for i, log in enumerate(self.logs):
            print(f"\t[{i}] - [{log['timestamp']}] ==({log['balance']}$)==> {log['message']}\n")

        input("\n\tPress <enter> to continue...")


    # Save logs list
    def saveLogs(self):
        # Appending new logs
        with open("./account_logs.txt", "w") as fd:
            fd.write(f"=======================[ Log saved on {datetime.now().strftime(r'%d-%m-%Y at %H:%M:%S')} ]=====================\n")
            for line in self.logs:
                fd.write(f"[{line['timestamp']}] - {line['message']} # Balance: {str(line['balance'])}$\n")

    # Load logs data
    def loadLogs(self):
        # Check and open logs file
        if path.exists("./account_logs.txt"):
            with open("./account_logs.txt", 'r') as fd:
                lines = fd.readlines()
            
            # Format logs
            logs = []
            for log in lines:
                # Omit headers
                if log[0] == '=': continue

                # Use same delimiter to split
                log = log.replace("#", '-').strip().split(" - ")
                logs.append({
                    "timestamp": log[0].strip("[]"),
                    "message": log[1],
                    "balance": int(log[2].strip("Balance: $"))
                })

            # Join logs
            self.logs += logs

            # Load balance
            self.balance = self.logs[-1]['balance'] if len(self.logs) else 0
            


    # Asks the user for an input
    def menuMgr(self):
        opt = input(f"\n\t    Pleate enter a valir option [1-{len(self.menuOptions)}]: ")
        
        self.clean()

        # ----------- MENU ----------
        if opt == "1":
            amount = int(input("\n\t\tEnter the amount to deposit --> "))
            self.deposit(amount)

        elif opt == "2":
            amount = int(input("\n\t\tEnter the amount to withdraw --> "))
            self.withdraw(amount)

        elif opt == "3":
            dest = input("\n\n\tEnter the datination account ID: ")
            amount = int(input("\n\tEnter the amount of money you want to send: "))
            self.makeTransaction(dest, amount)

        elif opt == "4":
            self.printLogs()

        elif opt == "6":
            self.exitATM()

        else:
            input("\n\t[!] The option selected is not valid...")
        # --------------------------

        self.clean()


    # Exit handler
    def exitATM(self):
        self.newLog("[x] Exit ATM")
        self.saveLogs()
        self.active = False

    # Format log messages
    def newLog(self, msg):

        log = {
            "message": msg,
            "balance": self.balance,
            "timestamp": datetime.now().strftime(r"%d-%m-%Y / %H:%M:%S")
        }

        self.logs.append(log)

    # Print main menu
    def printMenu(self):
        print("""
            +----------------------------------------------------------------------------------+
            |       Welcome to PyATM - Account: %9s     %30s$  |
            |                                                                                  |
            |       Last log: %-64s |
            +----------------------------------------------------------------------------------+

            +===============[ Main menu ]===============>""" % (self.accountID, f"Current balance: {self.balance}", self.logs[-1]['message']))
            
        for i, option in enumerate(self.menuOptions):
            print(f"""            |
            +-[{i+1}]-> {option}""")

    def clean(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")


    def generateId(self):
        return ''.join([str(randint(0,9)) for i in range(9)])