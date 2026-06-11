'''Post monthly

This script defines a function called post_monthly_obs where an http request
is used to retrieve the subject IDs of all camera traps included in sagebrush,
and uses an http request to post an empty observation with longitude and
latitude (0,0) once every month with cougar vision to ensure the camera stays
active on sagebrush.
'''
from datetime import datetime, UTC
import requests
from post_obs import post_observation


def post_monthly_obs(token, auth, list_cam):
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

    url = 'https://sagebrush.pamdas.org/api/v1.0/subject/'
    url_2 = 'https://sagebrush.pamdas.org/api/v1.0/subjects/?name='

    current_time = datetime.now(UTC)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    cam_name = list(list_cam.values())

    for i in enumerate(cam_name):
        i = i[0]

        # get subject_id from camera name 
        temp_url = url_2 + cam_name[i]
        response = requests.get(temp_url, headers=hdr, timeout=10)
        response_json = response.json()
        # clear after every request
        temp_url = ''
        subject_id = response_json['data'][0]['id']

        # check that a source exists for the subject
        url_3 = url + subject_id + '/sources/'
        response = requests.get(url_3, headers=hdr, timeout=20)
        response_json = response.json()
        # clear after every get request
        url_3 = ''
        
        print("Camera name: ", cam_name[i], "Subject_id: ", subject_id)

        # check if a valid camera subject/source
        if (response_json['status']['message'] != 'Not Found'
                and response_json['data'] != []):
            post_observation(subject_id, "", formatted_time, hdr)
        else:
            print("Invalid subject ID. The subject was not found or "
                    "contained no data.")
