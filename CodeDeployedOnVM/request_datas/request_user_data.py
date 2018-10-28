import pyodbc
import time

'''
values to be send

server = 'adroit.database.windows.net'
database = 'codefundo-db'
username = 'Adroitadmin1'
password = 'Adroitpassword1'
driver= '{ODBC Driver 17 for SQL Server}'
'''

def request_user_location(server,database,username,password,driver):
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    userlat = 0.0
    userlon = 0.0

    cursor.execute("select * from location2 where id = \'917204432197\';")
    row = cursor.fetchone()

    userlat = float(row[1])
    userlon = float(row[2])
    
    print("--------------------accessing azure DB----------------------")
    print (str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3]))
    print("-------------------------------------------------------------")

    cursor.close()
    del cursor 
    cnxn.close() 
    
    return userlat,userlon

