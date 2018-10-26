import requests
import json

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)

class ArgumentMissmatchError(Exception):
    """Raised when the input value is larger than expected"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "ArgumentMissmatchError : arguments passed={} when only 3 are expected".format(self.value)

def _url(path):
    return 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude=23.731639&longitude=80.944012&maxradiuskm=2000&' + path

def request_earhtq_loction(*args):
    """
    give either input type:
            > minimum magnitude
            > start time, end time
            > minimum magnitude, start time, end time
    output:
            response object of the request.get()
    """
    length = len(args)
    if length==1:
        return requests.get(_url('minmagnitude={}'.format(*args)))
    if length==2:
        return requests.get(_url('starttime={}&endtime={}'.format(*args)))
    if length==3:
        return requests.get(_url('minmagnitude={}&starttime={}&endtime={}'.format(*args)))
    raise ArgumentMissmatchError(length)

def get_earthq_locations(ip):
    """
    takes a list of magnitude, start date, end date as input

    returns a list of {"lat": lat ,"lon": lon} of the earthquakes
    """
    resp = request_earhtq_loction(*ip)
    if resp.status_code != 200:
        # This means something went wrong.
        raise APIError(resp.status_code)

    data = resp.json()
    count = int(data['metadata']['count'])
    locations = [] 

    for i in range(count):
        lon,lat,_ = data['features'][i]['geometry']['coordinates']
        tsunami = data['features'][i]['properties']['tsunami']
        locations.append({"lat":lat,"lon":lon,"tsunami":tsunami})

    return locations