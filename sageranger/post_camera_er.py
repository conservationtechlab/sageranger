"""Post Camera ER

This module defines a script called post-camera which creates new cameras
in Earthranger that shows up on the map and returns the id of the camera trap.

takes in a list of names and coordinates of new camera traps,
posts the camera traps as sources and subjects on Earthranger as well as an
intial observation, and returns the source and subject id of the camera
traps uploaded.

Inputs:
    authorization: the auth token for ER as defined in config yml, this
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

from datetime import datetime
import requests
import pandas as pd
from sageranger.post_obs import post_observation


def post_camera():  # pylint: disable=too-many-locals
    """Adds Cameras to csv list of camera traps"""

    auth = input('input authorization: ')

    hdr = {
        'Authorization': auth,
        'Accept': 'application/json'
        }

    url = 'https://sagebrush.pamdas.org/api/v1.0/'

    df = pd.read_csv('/path/to/csv',
                     delimiter=' ',
                     header=0)

    cam = df.camera.tolist()
    lat = df.lat.tolist()
    longi = df.longi.tolist()

    for i in enumerate(cam):
        i = i[0]
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')

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

        url_2 = url + 'sources/'
        source = requests.post(url_2, headers=hdr, json=payload, timeout=10)
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

        url_3 = url + 'subjects/'
        subject = requests.post(url_3, headers=hdr, json=payload, timeout=10)
        subject_js = subject.json()
        subject_id = subject_js['data']['id']

        # after subject is created add location
        payload = {
            "assigned_range": {},
            "source": source_id,
            "source_type": "tracking-device",
            "additional": {},
            "location": {
                "latitude": lat[i],
                "longitude": longi[i]}
        }

        url_4 = url + 'subject/' + subject_id + '/sources/'
        requests.post(url_4, headers=hdr, json=payload, timeout=10)

        response = requests.get(url_4, headers=hdr, timeout=10)
        source_2 = response.json()

        post_observation(subject_id, "", formatted_time, hdr)

        print("\nsubject id: " + subject_id)
        print("source id: " + source_2['data'][0]['id'])
        print("camera trap " + cam[i] + " is uploaded to sagebrush\n")
