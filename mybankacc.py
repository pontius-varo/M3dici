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
        # owner name should be automatic, maybe?
        name = input("Insert your name >>> ")
        # There should be a if statement to determine account type..
        acct_type = input("What type of account would you like to open? >>> ")
        balance = input("Insert your balance >>> ")
        print("Give me a moment while I generate your account")
        newnum = TinyPassMaker()
        num = newnum.junta(newnum.neochar_add())

        new_account = (library.sqlite_cmds["NEWACCT"] % (name, acct_type, balance, num))

        execute_query(self.connection, new_account)
    
    # showallbalances is an admin command. Users cannot use it.
    # Fork this function in order to create a regular user function
    def showallBalances(self):
        IDs = execute_read_query(self.connection, "SELECT ACCTID from Accounts")
        Balances = execute_read_query(self.connection, "SELECT BALANCE from Accounts")
        ownernames = execute_read_query(self.connection, "SELECT OWNER from Accounts")
        types = execute_read_query(self.connection, "SELECT TYPE from Accounts")
        # Arrays used to store 'clean' strings
        # There should be a better way to do this! Maybe just clean up each string returned?
        n1 = []
        n2 = []
        n3 = []
        n4 = []

        # Local functions that will later become public/class functions
        def cleanlist(array1, array2, customstr):
            for element in array1:
                array2.append(customstr + str(element).replace(",","").replace("(","").replace(")","").replace("\'", ""))
                
        def display(array1, array2, array3, array4):
            x = 0
            while x < len(array1):
                print(array1[x], "  ", array2[x], "  ", array3[x], "  ", array4[x])
                x += 1

        cleanlist(ownernames, n1, "Name: ")
        cleanlist(types, n2, "Type: ")
        cleanlist(Balances, n3, "Balance:")
        cleanlist(IDs, n4, "ACCTID:")
        
        display(n1, n2, n3, n4)
    
    def autoMatic(self, option):
        acctid = input("Which account? >>> ")
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

        update_acct_bal = (library.sqlite_cmds["UPDATE"] % (choice, mal_amount, acctid))

        # In the future an implementation to prevent overdrafting is needed
        execute_query(self.connection, update_acct_bal)

        new_bal = execute_read_query(self.connection, library.sqlite_cmds["GETACCTBAL"] % acctid)

        for balance in new_bal:
            neobal = str(balance).replace("(", "").replace(")", "").replace(",", "")
            print("Your account, whose number is %s, now has a balance of: %s" % (acctid, neobal))
        
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
                # Using eval() until I can figure out a better way to do this
                eval("steve.%s" % library.commands[c])
        #else:
            #Why is is printing a million times?
            #print("I don't understand what that means")

input_taker()
