import requests
import json

client_id = '2BDhrnVDvkfwTzXi0AiLx'
client_secret = 'BndgWzAcdKCgAu78lOaaZ1KFen3MwKwEpQpQI0dq'

class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


def _urlgeojson():
    return 'https://api.aerisapi.com/tropicalcyclones/within?p=25.0,53.3,-8.8,104.4&filter=indian&fields=position,track,forecast,errorCone&limit=1&format=geojson&client_id=2BDhrnVDvkfwTzXi0AiLx&client_secret=BndgWzAcdKCgAu78lOaaZ1KFen3MwKwEpQpQI0dq'

# def _urljson():
#     return 'https://api.aerisapi.com/tropicalcyclones/within?p=25.0,53.3,-8.8,104.4&&filter=all&format=json&client_id=2BDhrnVDvkfwTzXi0AiLx&client_secret=BndgWzAcdKCgAu78lOaaZ1KFen3MwKwEpQpQI0dq'

def _urljson():
    return 'https://api.aerisapi.com/tropicalcyclones/?&filter=all&format=json&client_id=2BDhrnVDvkfwTzXi0AiLx&client_secret=BndgWzAcdKCgAu78lOaaZ1KFen3MwKwEpQpQI0dq'


def request_cyclone_loction():
    return requests.get(_urljson())

def get_cyclone_location():
    """
    returns a list of dictionaries containing
        'name'                  :   name of the cyclone
        'current_location'      :   current location list as [lat,lon]
        'track_coordinates'     :   list of track coordiantes as a list of [lat,lon]
        'forecast_coordinates'  :   list of forcasted coordiantes as a list of [lat,lon]
    """
    resp = request_cyclone_loction()
    if resp.status_code != 200:
        # This means something went wrong.
        raise APIError(resp.status_code)

    data = resp.json()

    current_cyclones = []
    cyclone_details = dict.fromkeys(['name','current_location','track_coordinates','forecast_coordinates'])

    if data['success']:
        # if data['error']['description'] != '':
        #     print("successful: %s" % (data['error']['description'])) 
        #     return current_cyclones
        count = len(data['response'])
        for r in range(count):
            name  = str(data['response'][r]['profile']['name'])
            current_lon,current_lat = data['response'][r]['position']['location']['coordinates']
            current_location = {"lat":float(current_lat),"lon":float(current_lon)}

            track_len = len(data['response'][r]['track'])
            track_coordinates = []
            for tc in range(track_len):
                track_lon,track_lat = data['response'][r]['track'][tc]['location']['coordinates']
                track_coordinates.append({"lat":float(track_lat),"lon":float(track_lon)})

            forecast_len = len(data['response'][r]['forecast'])
            forecast_coordinates = []
            for fc in range(forecast_len):
                forecast_lon,forecast_lat = data['response'][r]['forecast'][fc]['location']['coordinates']
                forecast_coordinates.append({"lat":float(forecast_lat),"lon":float(forecast_lon)})  

            # cyclone_details['name'] = name   
            # cyclone_details['current_location'] = current_location   
            # cyclone_details['track_coordinates'] = track_coordinates
            # cyclone_details['forecast_coordinates'] = forecast_coordinates
            x = {'name': name, 'current_location': current_location,'track_coordinates': track_coordinates,'forecast_coordinates':forecast_coordinates}
            # print("printing in 'request_cyclone_data' : ",cyclone_details)
            current_cyclones.append(x)
            # print(current_cyclones)
        # print(current_cyclones)
        return current_cyclones

    else:
        print("An error occurred: %s" % (data['error']['description']))

