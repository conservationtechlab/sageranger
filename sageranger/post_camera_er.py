'''Post Camera ER

This module defines a script called post-camera which creates new cameras
in Earthranger that shows up on the map and returns the id of the camera trap.

takes in a list of names and coordinates of new camera traps,
posts the camera traps as sources and subjects on Earthranger, and returns
the source and subject id of the camera traps uploaded.

Inputs:
token: unique token for ER to authenticate http request, defined in config
yml
authorization: the other auth token for ER as defined in config yml, this
was retrieved from the interactive api on ER
https://<YOUR INSTANCE>.pamdas.org/api/v1.0/docs/interactive/
csv: a csv file that contains camera name, longitude and latitude of the
camera trap with header ['camera', 'lat', 'long'] and white space as
delimiter. Use the following as a sample:
           camera lat long
           S010 0 0
           S020 0 0
           S030 0 0
           S040 0 0
Outputs:
prints out the subject id and source id of the uploaded camera trap.

'''

from datetime import datetime
import requests
import pandas as pd

token = input('input token: ')
auth = input('input authorization: ')

hdr = {
    'X-CSRFToken': token,
    'Authorization': auth,
    'Accept': 'application/json'
    }

URL = 'https://sagebrush.pamdas.org/api/v1.0/'

df = pd.read_csv('(put ur csv dir here)', delimiter=' ', header=0)
cam = df.camera.tolist()
lat = df.lat.tolist()
longi = df.longi.tolist()

for i in enumerate(cam):
    i = i[0]
    current_time = datetime.utcnow()
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    payload = {
        "content_type": "observations.subject",
        "name": cam[i],
        "subject_type": "stationary-object",
        "subject_subtype": "camera_trap",
        'created_at': formatted_time,
        'updated_at': formatted_time,
        "is_active": True,
        "last_position_status": {
            "last_voice_call_start_at": [],
            "radio_state_at": [],
            "radio_state": "na"},
        "user": None,
        "last_position": {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lat[i], longi[i]]}}
        }

    URL_2 = URL + 'subjects/'
    subject = requests.post(URL_2, headers=hdr, json=payload, timeout=10)
    subject_js = subject.json()
    subject_id = subject_js['data']['id']
    print("\nsubject id: " + subject_id)

    payload = {
        "source_type": "seismic",
        "manufacturer_id": cam[i],
        "model_name": cam[i],
        "additional": {},
        "provider": "cougar_vision",
        "subject": subject_id,
        "assigned_range": {}
    }

    URL_3 = URL + 'sources/'
    source = requests.post(URL_3, headers=hdr, json=payload, timeout=10)
    response_js = source.json()
    source_id = response_js['data']['id']

    payload = {
        "source": source_id,
        "subject": subject_id,
        "assigned_range": {}
    }

    URL_4 = URL + 'subject/'+subject_id+'/sources/'
    requests.post(URL_4, headers=hdr, json=payload, timeout=10)

    response = requests.get(URL_4, headers=hdr, timeout=10)
    source_2 = response.json()
    print('source id: ' + source_2['data'][0]['id'])
    print('camera trap ' + cam[i] + ' is uploaded to sagebrush\n')
