import pyodbc
import time
server = 'adroit.database.windows.net'
database = 'codefundo-db'
username = 'Adroitadmin1'
password = 'Adroitpassword1'
driver= '{ODBC Driver 17 for SQL Server}'
while(True):
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    # print(cursor.execute("insert into location values ('111111',15.1,70.1);"))

    # print(cursor.execute("delete from location;"))
    # print(cursor.execute("drop location"))

    cursor.execute("select * from location2;")
    row = cursor.fetchone()
    while row:
        print (str(row[0]) + " " + str(row[1])+" "+str(row[2])+" "+str(row[3]))
        row = cursor.fetchone()

    print("\n----------------------------\n")
    cursor.close()
    del cursor 
    cnxn.close() 
    time.sleep(2)


# cnxn.commit()