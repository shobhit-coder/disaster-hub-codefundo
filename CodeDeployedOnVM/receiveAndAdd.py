import pyodbc
import urllib.request
import urllib.parse
import json
import time
from twilio.rest import Client
# import pprint


server = 'adroit.database.windows.net'          #for DB
database = 'codefundo-db'
username = 'Adroitadmin1'
password = 'Adroitpassword1'
driver= '{ODBC Driver 17 for SQL Server}'

account_sid = 'ACf13da2763effb648ca4fdb79cddb6e6a'  #for twilio
auth_token = '1e39d724fe31ab9250648ed01b783216'
client = Client(account_sid, auth_token)


sent=list()
notsendfirsttime=0
def getMessages(apikey, inboxID):
    data =  urllib.parse.urlencode({'apikey': apikey, 'inbox_id' : inboxID})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/get_messages/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return(fr)
 
while(True): 
    resp =  getMessages('EdsH25HMkSI-AAaVOr7P1ypRh2IzWGEtmAAYRsGiiQ', 10)
    my_json = resp.decode('utf8')

    data = json.loads(my_json)
    # print(resp)
    if 'errors' in data:
        if data["errors"][0]["message"]==' No messages found':
            print('No messages yet')
            continue
    count = int(data['num_messages'])
    
    for i in range(count):
        lat=data['messages'][i]['message'][6:].split(',')[0]
        lon=data['messages'][i]['message'][6:].split(',')[1]
        status=data['messages'][i]['message'][6:].split(',')[2]
        number=data['messages'][i]['number']
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = cnxn.cursor()
        print(number)
        cursor.execute("select count(*) from location2 where id=\'"+str(number)+"\';")
        #cursor.execute("insert into location2 values (\'"+str(number)+"\',"+lat+","+lon+",\'"+status[0]+"\');")
        flag=0
        row = cursor.fetchone()
        while row:
            # print("row0 is"+str(row[0])+" "+str(row[1])+" "+str(row[2])+" "+str(row[3])+" "+str(row[4]))
            # for x in row:
            #     print(str(x)+ " ")
            if row[0]==0:
                flag=1
            # print (str(row[0]) + " " + str(row[1])+" "+str(row[2]))
            row = cursor.fetchone()
        # print("flag is"+str(flag))
        if flag==1:
            if number not in sent:
                cursor.execute("insert into location2 values (\'"+str(number)+"\',"+lat+","+lon+",\'"+status[0]+"\',\'*\');")
                message = client.messages \
                    .create(
                        body="Your response has been recorded and the information will be displayed on our maps.\nTeam Adroit Staysafe",
                        from_='+14302160382',
                        to='+917204432197'        #due to trial account regulations, only to this number
                    )
                sent.append(number)
                # print(message.sid)
                # print(message)      
        else:
            if number not in sent:
                if notsendfirsttime==1:
                    cursor.execute("udpate location2 set flag=\'"+status[0]+"\' where id=\'"+str(number)+"\'")
                    message = client.messages \
                        .create(
                            body="Your response has already been received and stored.\nTeam Adroit Staysafe :)",
                            from_='+14302160382',
                            to='+917204432197'      #due to trial account regulations, only to this number
                        )
                
                print(':)')
                sent.append(number)
                

        cnxn.commit()

        time.sleep(2)
        
    notsendfirsttime=1
        # print("insert ignore into location2 values (\'"+str(number)+"\',"+lat+","+lon+");")
        
        # cursor.execute("insert or ignore into location2 values (\'"+str(number)+"\',"+lat+","+lon+",\'"+status[0]+"\');")

        # print(cursor.execute("delete from location;"))

        # cursor.execute("select * from location;")
        # 
        


    cursor.close()
    del cursor 
    cnxn.close() 


#send sms to +91 9220592205
#message begin with 'JPE93 '