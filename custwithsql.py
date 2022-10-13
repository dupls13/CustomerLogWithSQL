import string
from tkinter import *
import sqlite3

"""         Start               """
root = Tk()
root.title("Customer Log")


"""         Functions           """

# Gets phone input and turns to string 
def numberGrab():
    global currentClient
    currentClient = phoneEntry.get()
    currentClient = str(currentClient)

# Gets reason input and turns to string 
def reasonGrab():
    global currentReason
    currentReason = reasonEntry.get()
    currentReason = str(currentReason)

# Connect to database 
def connect_sql():
    
    # Create database or connect to one 
    conn = sqlite3.connect('custlog.db')
    # Create cursor for database
    c = conn.cursor()
    
    
    # Create table 
    c.execute(""" CREATE TABLE IF NOT EXISTS custlogs (
        phonenumber string,
        reason string
        )""")
    
    # Insert into table 
    c.execute(""" INSERT INTO custlogs VALUES( :phonenumber, :reason)""",
              {
                  'phonenumber': currentClient,
                  'reason': currentReason
              })
    
    
    # Commit changes to database
    conn.commit()
    
    # Close connection 
    conn.close()
    
    # Delete entries from 
    phoneEntry.delete(0, END)
    reasonEntry.delete(0, END)
    
# Create query function 
def query_entries():
    
    # Database requirements
    conn = sqlite3.connect('custlog.db')
    c = conn.cursor()
    
    # Query the database
    c.execute(" SELECT * FROM custlogs")
    logs = c.fetchall()
    
    # Clear the left text before displaying table
    clientDisplay.delete("1.0", "end")
    
    # Separates entries and converts to strings
    print_log = ''
    for log in logs: 
        print_log += str(log[0]) + " " + str(log[1]) + "\n"
    
    # Inserts table into display area
    clientDisplay.insert(END, print_log)

    # Database requirements 
    conn.commit()
    conn.close()


def deleteAll(): 
    conn = sqlite3.connect('custlog.db')
    c = conn.cursor()
    
    # Deletes entire table
    c.execute(""" DROP TABLE custlogs """)
    
    clientDisplay.delete('1.0', 'end')
    
    conn.commit()
    conn.close()




# Runs all functions when Submit button is pressed  
def runGrabs():
    numberGrab()
    reasonGrab()
    connect_sql()
    query_entries()



"""         Display         """


""" ------ Left Side -------- """

#Phone number area
phoneNumber = Label(root, text = "Client's Phone Number: ")
phoneNumber.grid(row = 0, column = 0)

phoneEntry = Entry(root, width = 30, borderwidth = 5)
phoneEntry.grid(row=1, column = 0)

# Reason Area
reason = Label(root, text= "Problem: ")
reason.grid(row=2 , column = 0)

reasonEntry = Entry(root, width = 30, borderwidth = 5)
reasonEntry.grid(row = 3, column = 0)

#Submit Button 
submitButton = Button(root, text = "Submit", command= runGrabs)
submitButton.grid(row = 4, column = 0)

deleteButton = Button(root, text = "Delete table", command = deleteAll)
deleteButton.grid(row = 5, column = 0) 



""" ----- Middle Gab -----"""
blankText = Label(root,text = "                  ")
blankText.grid(row=0, column=1)


""" ----- Right Side -----"""

#Right Title 
clientlist = Label(root, text="Client list")
clientlist.grid(row= 0, column = 2, padx = 20)

#Left Display List 
clientDisplay = Text(root)
clientDisplay.grid(row =1, column = 2, rowspan=8, ipady = 50)



"""      Finish tkinter   """
root.mainloop()

