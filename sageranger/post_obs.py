"""Posts Observations

This file is responsible for posting 
an observation to earthranger. It is 
used by post cougar_log, post_camera,
and post_monthly.

"""

import requests

def post_observation(subject_id, label, time, hdr):
    """ Post Observation

    This function posts an observation using the subject_id,
    label of animal, time of observation, and the authorization
    token.

    Args:
        subject_id (str): the id of the subject from earthranger
        label (str): the name of the animal identified
        time (str): formatted time of the observation
        hdr (dict): authorization and permission to access earthrangers
            api (obtained from the interactive api 
            https://<YOUR INSTANCE>.pamdas.org/api/v1.0/docs/interactive/ )

    """

    url = 'https://sagebrush.pamdas.org/api/v1.0/' 

    url_3 = url + 'subject/' + subject_id + '/sources/' 
    response = requests.get(url_3, headers=hdr, timeout=10)
    response_json = response.json()
  
    source_id = response_json['data'][0]['id']
    payload = {
        "location": {"longitude": 0, 
                     "latitude": 0},
                     "recorded_at": time,
                     "source": source_id,
                     "device_status_properties":
                     [{"value": "test", "label": "animal", "units": ""}],
                     "additional": {"animal": label}
        }
    url_5 = url + 'observations/'
    obs = requests.post(url_5, headers=hdr, json=payload, timeout=20)
    print("Observation response: ", obs)
    



