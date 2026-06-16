"""Post monthly

This script defines a function called post_monthly_obs where an http request
is used to retrieve the subject IDs of all camera traps included in sagebrush,
and uses an http request to post an empty observation with longitude and
latitude (0,0) once every month with cougar vision to ensure the camera stays
active on sagebrush.
"""
from datetime import datetime, UTC
import requests
from sageranger.post_obs import post_observation


def post_monthly_obs(auth, list_cam):
    """post_monthly_obs
    This function gets the subject id of camera traps and posts observations
    onto earthranger
    Args:
        auth (str): token for api calls as specified in config yml 'str'
        list_cam (dict): dictionary of camera names and strikeforce_id
            from the config file
    Returns:
        prints the http request response code to tell us if the call worked
             or not as well as camera name and subject id
    """
    hdr = {
        'Authorization': auth,
        'Accept': 'application/json'
    }

    url_1 = 'https://sagebrush.pamdas.org/api/v1.0/subjects/?name='
    url_2 = 'https://sagebrush.pamdas.org/api/v1.0/subject/'

    current_time = datetime.now(UTC)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    cam_name = list(list_cam.values())

    for i in enumerate(cam_name):
        i = i[0]
        # get subject_id from camera name
        url_cam = url_1 + cam_name[i]
        response = requests.get(url_cam, headers=hdr, timeout=10)
        response_json = response.json()
        # clear after every request
        url_cam = ''
        subject_id = response_json['data'][0]['id']

        # check that a source exists for the subject
        url_src = url_2 + subject_id + '/sources/'
        response = requests.get(url_src, headers=hdr, timeout=20)
        response_json = response.json()
        # clear after every get request
        url_src = ''

        print("Camera name: ", cam_name[i], "Subject_id: ", subject_id)

        # check if a valid camera subject/source
        if (response_json['status']['message'] != 'Not Found'
                and response_json['data'] != []):
            post_observation(subject_id, "", formatted_time, hdr)
        else:
            print("Invalid subject ID. The subject was not found or "
                  "contained no data.")
