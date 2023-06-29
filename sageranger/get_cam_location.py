'''Post monthly

This script defines a function called post_monthly_obs where an http request
is used to retrieve the subject IDs of all camera traps included in sagebrush,
and uses an http request to post an empty observation with longitude and
latitude (0,0) once every month with cougar vision to ensure the camera stays
active on sagebrush.
'''
from datetime import datetime as dt
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
    headers = {
        'X-CSRFToken': token,
        'Authorization': auth,
        'Accept': 'application/json'
    }

    url_obs = 'https://sagebrush.pamdas.org/api/v1.0/observations/'
    url_s = 'https://sagebrush.pamdas.org/api/v1.0/sources/'

    current_time = dt.utcnow()
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    response = requests.get(url_s, headers=headers, timeout=10)
    response_json = response.json()
    results = response_json['data']['results']

    for i in enumerate(results):
        i = i[0]
        if results[i]['manufacturer_id'][:2] == 'B0':
            obs_data = {
                "location": {"longitude": 0, "latitude": 0},
                "recorded_at": formatted_time,
                "source": results[i]['id'],
                "device_status_properties":
                [{"value": 'test', "label": "animal", "units": ""}],
                "additional": {"animal": 'test'}
                }
            response = requests.post(url_obs, headers=headers, json=obs_data, timeout=10)
            print(response)
