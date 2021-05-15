import sys
import library
from sqlite3 import Error, connect
from random import randrange

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
    
    # showallbalances is an admin command. Users cannot use it.
    def showallBalances(self):
        IDs = execute_read_query(self.connection, "SELECT ACCOUNTNUM from Accounts")
        Balances = execute_read_query(self.connection, "SELECT BALANCE from Accounts")

        # Arrays used to store 'clean' strings
        n1 = []
        n2 = []

        # Local functions that will later become public/class functions
        def cleanlist(array1, array2, customstr):
            for element in array1:
                array2.append(customstr + str(element).replace(",","").replace("(","").replace(")",""))
                
        def display(array1, array2):
            x = 0
            y = 0
            while x < len(array1) and y < len(array2):
                print(array1[x], "", array2[y])
                x += 1
                y += 1

        cleanlist(IDs, n1, "ACCTNUM:")
        cleanlist(Balances, n2, "Balance:")

        display(n1, n2)
    
    def autoMatic(self, option):
        acctnum = input("Which account? >>> ")
        mal_amount = input("What amount? >>> ")
        print("one moment")

        choice = ""

        if option == "W":
            choice = "-"
        elif option == "D":
            choice = "+"
        else:
            print("u w0t m8?")
            return

        update_acct_bal = ("""
        UPDATE
            Accounts
        SET
            BALANCE=(BALANCE %s %s)
        WHERE
            ACCOUNTNUM = %s
        """ % (choice, mal_amount, acctnum))

        # In the future an implementation to prevent overdrafting is needed
        execute_query(self.connection, update_acct_bal)

        new_bal = execute_read_query(self.connection, "SELECT BALANCE FROM Accounts WHERE ACCOUNTNUM = %s;" % acctnum)

        for balance in new_bal:
            neobal = str(balance).replace("(", "").replace(")", "").replace(",", "")
            print("Your account, whose number is %s, now has a balance of: %s" % (acctnum, neobal))
        
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
                #result = getattr(steve, library.commands[c])()
                eval("steve.%s" % library.commands[c])
        #else:
            #Why is is printing a million times?
            #print("I don't understand what that means")


input_taker()
