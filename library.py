title = "" #Title of the application

# "Key" : function
commands = {"HELP": "myhelp()", "NEWACCOUNT": "newAccount()",
            "SHOWBALANCE": "showbalances()", "WITHDRAW": "autoMatic(\"W\")",
            "DEPOSIT": "autoMatic(\"D\")", "SHOWTRANSACTIONS": "showTransactions()",
            "QUIT" : "quit()", "SHOWALLBALANCES": "showallBalances()"}
#admin_commands = {"SHOWALLBALANCES": "showallBalances()"}


strings = {"HP" : """Current commands are newaccount, showallbalances, withdraw, deposit, quit, and showtransactions"""}

sqlite_cmds = {"UPDATE" : "UPDATE Accounts SET BALANCE=(BALANCE %s %s) WHERE ACCTID = %s;", "GETACCTBAL" : """SELECT BALANCE FROM
        Accounts WHERE ACCTID = %s;""", "NEWACCT" : "INSERT INTO Accounts (OWNER, TYPE, BALANCE, ACCTID) VALUES (\'%s\', \'%s\', %s, %s)"}
