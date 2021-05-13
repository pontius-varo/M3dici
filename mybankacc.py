import sys
import library
from sqlite3 import Error, connect
from random import randrange
#from sqlite3 import Error, connect, cursor
#^ imports sqlite and Error class from that library

def create_connection(path):
    #^Defines function that accepts a path to a sql database
    connection = None
    try:
        # no need for "sqlite3.connect", as I've already imported connect
        connection = connect(path)
        #^ uses "connect" function from sqlite database to actually connect to database
        print("Connection to Database established.")
    except Error as e:
        print("The error \'{e}\' occurred. Are you sure that the db file exists?")
        return

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
        
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occured")


class BankManager:

    def __init__(self, connection):
        self.connection = connection

    def newAccount(self):
        #name = input("Insert your name >>> ") <-- add to line 55 "NAME"
        balance = input("Insert your balance >>> ")
        print("Give me a moment while I generate your account")
        newnum = TinyPassMaker()
        num = newnum.junta(newnum.neochar_add())
        new_account = ("""
        INSERT INTO
            Accounts (ACCOUNTNUM, BALANCE)
        VALUES
            (%s, %s)
        """ % (num, balance))

        print(new_account)
        execute_query(self.connection, new_account)

    #def showallBalances(self):
        #shows all amounts in BALANCE
        #select_account = "SELECT * FROM Accounts;"
        #account = execute_read_query(self.connection, select_account)
        
        #select_ID = execute_read_query(self.connection, "SELECT ACCOUNTNUM from Accounts")
        #select_bal = execute_read_query(self.connection, "SELECT BALANCE from Accounts")
        #psudoshow = "ID:" + select_ID + "|" + "Balance:" + select_bal
        #print(select_ID)
        #print(select_bal)
        
        #for acct in psudoshow:
           # print(acct)
    def showallBalances(self):
        IDs = execute_read_query(self.connection, "SELECT ACCOUNTNUM from Accounts")
        Balances = execute_read_query(self.connection, "SELECT BALANCE from Accounts")

        #for ID in IDs:
            # Not pretty, but it works
            #tempID = str(ID).replace(",","").replace("(","").replace(")","")

            #cleanID = "ACCTNUM:" + tempID
            #print(cleanID)
        
        # This throws duplicate IDs with repeating balances!
        for ID in IDs:
            for Bal in Balances:
                cleanID = str(ID).replace(",","").replace("(","").replace(")","")
                cleanBal = str(Bal).replace(",","").replace("(","").replace(")","")
                print("ACCTNUM|"+ cleanID + "|" + "Balance|" + cleanBal)

    def withdraw(self):
        acctnum = input("Insert your account number. >>> ")
        retiro = input("What ammount are you withdrawing? >>> ")
        print("One moment please.")

        update_account_balance = ("""
        UPDATE
            Accounts
        SET
            BALANCE=(BALANCE-%s)
        WHERE
            ACCOUNTNUM = %s
        """ % (retiro, acctnum))

        execute_query(self.connection, update_account_balance)

        select_account_balance = ("SELECT BALANCE FROM Accounts WHERE ACCOUNTNUM = %s;" % (acctnum))

        new_balance = execute_read_query(self.connection, select_account_balance)

        for balance in new_balance:
            print("Your account, whose number is %s, now has a balance of: %s" % (acctnum, balance))

    def deposit(self):
        return

    def myhelp(self):
        print(library.strings["HP"])

    def quit(self):
        print("Until next time.")
        sys.exit()

class RecordKeeper(BankManager):

    def __init__(self):
        #Takes a certain account number
        return

    def showTransactions(self): #Pass the account number through!
        #shows all the data in the 'transactions' table
        #But only those associated with a certain account number
        return

class TinyPassMaker():

    def __init__(self):
        # This looks really disgusting, and rather uncomfortable
        #return self.junta(self.neochar_add())
        pass

    def neochar_add(self):
        #Did my number choice really need to be in an array?
        nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        z = 0
        usernum = []

        while z < 4:
            y = randrange(len(nums))
            usernum.append(nums[y])
            z += 1

        return usernum

    def junta(self, usernum):
        newnum = " "
        return self.remove(newnum.join(usernum))

    def remove(self, string):
        return string.replace(" ","")

#V This is really weird! Please find a way to make this more presentable
#print(newnum.junta(newnum.neochar_add()))

def input_taker():
    bank = create_connection("db/banco.db")
    active = True
    #print an intro from a library
    print("Test")

    while active:
        #V Creates BankManager object
        steve = BankManager(bank)
        cmd = input("$ ")
        #Fetch command list from library
        for c in library.commands:
            if cmd.upper() == c:
                #Thank God for the getattr function. It feeds a string into an object, as if I'm calling a module
                result = getattr(steve, library.commands[c])()
        #else:
            #Why is is printing a million times?
            #print("I don't understand what that means")


input_taker()
