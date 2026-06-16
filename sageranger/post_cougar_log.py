"""Post Animal of Interest Log

This module defines a function called is_target which adds an observation
to a specific camera in Earthranger with time and the fact that an animal of
interest was detected.
"""
from datetime import datetime, UTC
import requests
from post_obs import post_observation


def is_target(cam_name, authorization, label):
    """Target animal historical log

    This function takes in the camera name and http api tokens only if
    an animal of interest was detected, creates an observation for specific
    camera it was detected at and logs the time so that there is a historical
    backlog for each camera of all its target animal detections.

    Args:
    cam_name: a string of the specific name of the camera that image came from
        as it also is in Earthranger
    token: unique token- ER to authenticate http request, defined in config yml
    authorization: other auth token for ER as defined in config yml, this was
        retrieved from the interactive api on ER
        https://<YOUR INSTANCE>.pamdas.org/api/v1.0/docs/interactive/
    """
    headers = {
        'Authorization': authorization,
        'Accept': 'application/json'
    }

    current_time = datetime.now(UTC)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    url = 'https://sagebrush.pamdas.org/api/v1.0/subjects/?name=' + cam_name

    response = requests.get(url, headers=headers, timeout=10)
    response_json = response.json()

    subject_id = response_json['data'][0]['id']

    post_observation(subject_id, label, formatted_time, headers)
