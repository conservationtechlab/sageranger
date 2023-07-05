'''Post Camera ER

This module defines a function called post-camera which creates new cameras
in Earthranger that shows up on the map and returns the id of the camera trap.

'''

from datetime import datetime
import requests


def post_camera(cam, cord, token, auth):
    '''Post camera

    This function takes in a list of names and coordinates of new camera traps,
    posts the camera traps as sources and subjects on Earthranger, and returns
    the source and subject id of the camera traps uploaded.

    Args:
    camera: a list of all the names of the new camera traps that need
    to be uploaded to Earthranger
    cord: a list of all the coordinates of the new camera traps that need
    to be uploaded to Earthranger, in the form of [latitude,longitude]
    token: unique token for ER to authenticate http request, defined in config
    yml
    authorization: the other auth token for ER as defined in config yml, this
    was retrieved from the interactive api on ER
    https://<YOUR INSTANCE>.pamdas.org/api/v1.0/docs/interactive/

    Returns: the two unique ids of the camera trap as subject and source
    on Earthranger
    '''

    hdr = {
        'X-CSRFToken': token,
        'Authorization': auth,
        'Accept': 'application/json'
    }

    url = 'https://sagebrush.pamdas.org/api/v1.0/'

    for i in enumerate(cord):
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
                    "coordinates": [cord[i][0], cord[i][1]]}}
        }

        url_2 = url + 'subjects/'
        subject = requests.post(url_2, headers=hdr, json=payload, timeout=10)
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

        url_3 = url + 'sources/'
        source = requests.post(url_3, headers=hdr, json=payload, timeout=10)
        response_js = source.json()
        source_id = response_js['data']['id']

        payload = {
            "source": source_id,
            "subject": subject_id,
            "assigned_range": {}
        }

        url_4 = url + 'subject/'+subject_id+'/sources/'
        requests.post(url_4, headers=hdr, json=payload, timeout=10)

        response = requests.get(url_4, headers=hdr, timeout=10)
        source_2 = response.json()
        print('source id: ' + source_2['data'][0]['id'])
        print('camera trap ' + cam[i] + ' is uploaded to sagebrush\n')
