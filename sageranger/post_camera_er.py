"""Post Camera ER

This module defines a script called post-camera which creates new cameras
in Earthranger that shows up on the map and returns the id of the camera trap.

takes in a list of names and coordinates of new camera traps,
posts the camera traps as sources and subjects on Earthranger as well as an
intial observation, and returns the source and subject id of the camera 
traps uploaded.

Inputs:

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

"""

from datetime import datetime, UTC
import requests
import pandas as pd


auth = input('Input authorization: ')

hdr = {
    'Authorization': auth,
    'Accept': 'application/json'
    }

URL = 'https://sagebrush.pamdas.org/api/v1.0/'

df = pd.read_csv('/home/montse/sageranger/sageranger/camera_test.csv', delimiter=' ', header=0)
cam = df.camera.tolist()
lat = df.lat.tolist()
longi = df.longi.tolist()

for i in enumerate(cam):
    i = i[0]
    current_time = datetime.now(UTC)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    # first create a source 
    payload = {
        "source_type": "seismic",
        "manufacturer_id": cam[i],
        "model_name": cam[i],
        "additional": {},
        "provider": "cougar_vision",
        "subject": {
            "name": cam[i],
            "subject_subtype": "camera_trap"
        },
        "assigned_range": {}
    }

    URL_2 = URL + 'sources/'
    source = requests.post(URL_2, headers=hdr, json=payload, timeout=10)
    response_js = source.json()
    source_id = response_js['data']['id']

    # Then create a subject
    payload = {
        "content_type": "observations.subject",
        "name": cam[i],
        "subject_type": "stationary-object",
        "subject_subtype": "camera_trap",
        "additional": {},
        "created_at": formatted_time,
        "updated_at": formatted_time,
        "is_active": 1,
        }

    URL_3 = URL + 'subjects/'
    subject = requests.post(URL_3, headers=hdr, json=payload, timeout=10)
    subject_js = subject.json()
    subject_id = subject_js['data']['id']

    # add the location (cannot add location when creating a subject)
    payload = {
        "assigned_range": {},
        "source": source_id,
        "source_type": "tracking-device",
        "additional": {},
        "location":{
        "latitude": lat[i],
        "longitude": longi[i]
        }
    }

    URL_4 = URL + 'subject/'+ subject_id+'/sources/'
    requests.post(URL_4, headers=hdr, json=payload, timeout=10)
    response = requests.get(URL_4, headers=hdr, timeout=10)
    source_2 = response.json()

    # post a test observation to put camera on the map
    # long/lat can be 0 because the location of the stationary
    # object has already been set
    payload = {
            "location": {
                "longitude": 0,
                  "latitude": 0},
            "recorded_at": formatted_time,
            "source": source_id,
             "device_status_properties":[{
                 "value": "test", 
                 "label": "animal", 
                 "units": ""}],
            "additional": {
                "animal": 'test'}
     }
    
    URL_5 = URL + 'observations/'
    obs = requests.post(URL_5, headers=hdr, json=payload, timeout=10)
    
    print("\nsubject id: " + subject_id)
    print("source id: " + source_2['data'][0]['id'])
    print("camera trap " + cam[i] + " is uploaded to sagebrush\n")
