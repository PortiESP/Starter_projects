from atm_class import *


# =====================================[ Main loop ]=====================================
atm = ATM()

while atm.active:
    atm.printMenu()
    atm.menuMgr()

atm.printLogs()