'''Post monthly

This script defines a function called post_monthly_obs where an http request
is used to retrieve the subject IDs of all camera traps included in sagebrush,
and uses an http request to post an empty observation with longitude and
latitude (0,0) once every month with cougar vision to ensure the camera stays
active on sagebrush.
'''
from datetime import datetime
import requests


def post_monthly_obs(token, auth):
    '''post_monthly_obs
    This function gets the subject id of camera traps and posts observations
    onto earthranger
    Args:
        token: the token for api calls in earthranger 'str'
        auth: another token for api calls as specified in config yml 'str'
    Returns: the http request response code to tell us if the call worked
    or not
    '''
    hdr = {
        'X-CSRFToken': token,
        'Authorization': auth,
        'Accept': 'application/json'
    }

    url = 'https://sagebrush.pamdas.org/api/v1.0/observations/'
    url_2 = 'https://sagebrush.pamdas.org/api/v1.0/subjects/'
    url_3 = 'https://sagebrush.pamdas.org/api/v1.0/subject/'
    current_time = datetime.utcnow()
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    response = requests.get(url_2, headers=hdr, timeout=10)
    response_json = response.json()
    results = response_json['data']

    for i in enumerate(results):
        i = i[0]
        if results[i]['subject_subtype'] == 'camera_trap':
            subject_id = results[i]['id']
            manu_id = results[i]['name']
            print(manu_id)
            url_3 = url_3 + subject_id + '/sources/'
            response = requests.get(url_3, headers=hdr, timeout=10)
            response_json = response.json()
            if response_json['data'] != []:
                source_id = response_json['data'][0]['id']
                data = {
                        "location": {"longitude": 0, "latitude": 0},
                        "recorded_at": formatted_time,
                        "source": source_id,
                        "device_status_properties":
                        [{"value": 'test', "label": "animal", "units": ""}],
                        "additional": {"animal": 'test'}}
                obs = requests.post(url, headers=hdr, json=data, timeout=10)
                print(obs)
