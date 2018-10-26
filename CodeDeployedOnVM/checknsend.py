import firebase_admin
import pyodbc
import time
from firebase_admin import messaging
from firebase_admin import credentials
from twilio.rest import Client
from request_datas.request_cyclone_data import get_cyclone_location
from request_datas.request_earthq_data import get_earthq_locations
from request_datas.request_user_data import request_user_location
from time import sleep

def send_online(registration_token,senddict):
    # See documentation on defining a message payload.
    message = messaging.Message(
        topic='news',
        data={
            "data" : str(senddict)
        },
        # token=registration_token
    )

    # Send a message to the device corresponding to the provided
    # registration token.
    response = messaging.send(message)
    # Response is a message ID string.
    print("-------------------------online------------------------------")
    print('Successfully sent message:', response)
    print("-------------------------------------------------------------")


def send_sms(client,userlat,userlon,senddict):
    eq = ''
    cy = ''
    cydatalist = senddict["cydata"]
    eqlocations = senddict["eqlocation"]

    for d in eqlocations:
        lat = d["lat"]
        lon = d["lon"]
        if abs(userlat-lat)<4 and abs(userlon-lon)<4:
            eq = "earthquake near you"
            break

    for d in cydatalist:
        lat = d["cylocation"]["lat"]
        lon = d["cylocation"]["lon"]
        if abs(userlat-lat)<5 and abs(userlon-lon)<5:
            cy = "cyclone apporaching you"
            break
        
    if eq != '' or cy != '':
        message = client.messages \
                    .create(
                        body="ALERT!"+"\n"+eq+"\n"+cy+"Be safe, Team Adroit",
                        from_='+14302160382',
                        to='+917204432197'
                    )
        print("-----------------------------sms----------------------------")
        print(message.sid)
        print(message)
        print("-------------------------------------------------------------")


def process_data(eq_details):
    alert = False
    global prev
    cur = set()
    eqlocations = get_earthq_locations(eq_details)
    cylocations = get_cyclone_location()

    for loc in eqlocations:
        cur.add(loc["lat"])
        cur.add(loc["lon"])

    senddict = dict.fromkeys(["eqlocation","cydata"])
    cydatadict = dict.fromkeys(["cylocation","cytrack","cyforecast"])
    # list of cyclones with above specified data
    cydatalist = []

    if cylocations != []:
        for cydata in cylocations:
            # cydatadict["cylocation"] = cydata["current_location"]
            cur.add(cydata["current_location"]["lat"])
            cur.add(cydata["current_location"]["lon"])
            # cydatadict["cytrack"] = cydata["track_coordinates"]
            # cydatadict["cyforecast"] = cydata["forecast_coordinates"]
            x = {"cylocation": cydata["current_location"],"cytrack": cydata["track_coordinates"],"cyforecast":cydata["forecast_coordinates"]}
            cydatalist.append(x)

    senddict["cydata"] = cydatalist 
    senddict["eqlocation"] = eqlocations

    print("-----------------------incoming data-------------------------")
    print(senddict)
    print("-------------------------------------------------------------")

    if (cur-prev == set()) and (prev-cur == set()):
        alert = False
        print("\nNo Alert")
    else:
        alert = True
    
    prev = cur
    cur = set()

    return senddict,alert

def init_prev(eq_details):
    prev = set()
    cydatalist = get_cyclone_location()
    eqlocations = get_earthq_locations(eq_details)

    for d in eqlocations:
        prev.add(d["lat"])
        prev.add(d["lon"])
        
    for l in cydatalist:
        prev.add(l['current_location']["lat"])
        prev.add(l['current_location']["lon"])
        
    return prev

# for connecting to firebase
cred = credentials.Certificate("codefundotest2-firebase-adminsdk-877hq-a781dd3c3d.json")
firebase_admin.initialize_app(cred)
registration_token = 'eUEVo327wHc:APA91bFj_GYDWywvw7RE_jpYoNt2jPZg6k8aZg7fCur1ukw7eVWAz-W29MCw3feI-lb_brNbQtVPeNa5n-SithrEElI45_g-Uogsw60DU81Nv2WLe803oQueEZQI2-_j3R1epGjvCn7r'

# for connecting to azure SQL database
server = 'adroit.database.windows.net'
database = 'codefundo-db'
username = 'Adroitadmin1'
password = 'Adroitpassword1'
driver= '{ODBC Driver 17 for SQL Server}'

# for sms services
account_sid = 'ACf13da2763effb648ca4fdb79cddb6e6a'
auth_token = '1e39d724fe31ab9250648ed01b783216'
client = Client(account_sid, auth_token)

# earthquake details
eq_details = [5,'','']

# whether new calamity has happened or not
alert = False
# prev = init_prev(eq_details)
prev = set()

debug = 1

while True:
    alert = False
    while alert == False:
        senddict,alert = process_data(eq_details)
    else:
        send_online(registration_token,senddict)
        userlat,userlon = request_user_location(server,database,username,password,driver)
        send_sms(client,userlat,userlon,senddict)
    if debug == 1:
        break
    sleep(120)

# # process data and tell whether to send alert or not
# senddict,alert = process_data(eq_details)

# # send the cyclone and earthquake data online
# send_online(registration_token,senddict)

# # getting user loaction
# userlat,userlon = request_user_location(server,database,username,password,driver)

# # checking if calamaity is near user and sending an Alert sms
# send_sms(client,userlat,userlon,senddict)



