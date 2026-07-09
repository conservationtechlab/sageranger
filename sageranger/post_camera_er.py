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

from datetime import datetime, UTC
import requests
import pandas as pd
from sageranger.unpack_info import get_config_info
from sageranger.sensor_class import SensorInfo
from sageranger.post_obs import post_observation


def post_camera():  # pylint: disable=too-many-locals
    """Adds Cameras to csv list of camera traps"""

    
    config = get_config_info(SensorInfo)

    hdr = {
        'Authorization': config.auth_token,
        'Accept': 'application/json'
        }

    url = 'https://sagebrush.pamdas.org/api/v1.0/'

    df = pd.read_csv(config.path_csv,
                     delimiter=' ',
                     header=0)

    sen = df.sensor.tolist()
    lat = df.lat.tolist()
    longi = df.longi.tolist()

    for i in enumerate(sen):
        i = i[0]
        current_time = datetime.now(UTC)
        formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

        # first create a source
        payload = {
            "source_type": config.source_type,
            "manufacturer_id": sen[i],
            "model_name": sen[i],
            "additional": {},
            "provider": config.provider,
            "subject": {
                "name": sen[i],
                "subject_subtype": config.subject_subtype
            },
            "assigned_range": {}
        }

        url_2 = url + 'sources/'
        source = requests.post(url_2, headers=hdr, json=payload, timeout=10)
        response_js = source.json()
        # print(response_js)
        source_id = response_js['data']['id']

        # Then create a subject
        payload = {
            "content_type": config.content_type,
            "name": sen[i],
            "subject_type": config.subject_type,
            "subject_subtype": config.subject_subtype,
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
            "source_type": config.source_type,
            "additional": {},
            "location": {
                "latitude": lat[i],
                "longitude": longi[i]}
        }

        url_4 = url + 'subject/' + subject_id + '/sources/'
        requests.post(url_4, headers=hdr, json=payload, timeout=10)

        response = requests.get(url_4, headers=hdr, timeout=10)
        source_2 = response.json()


        #get subject group id 
        url_5 =  url +'/subjectgroups/?group_name=' + config.group_name
        response = requests.get(url_5, headers=hdr, timeout=20)
        response_json = response.json()
        group_id = response_json['data'][0]['id']

        #post subject to subject group 
        payload = [{
            "id": subject_id,
            "name": sen[i],
            "subject_type": config.subject_type,
            "subject_subtype": config.subject_subtype,
            "additional": {},
            "created_at": formatted_time,
            "updated_at": formatted_time,
            "is_active": 1,
            }]

        url_6 = url + 'subjectgroup/' + group_id + '/subjects'
        subject = requests.post(url_6, headers=hdr, json=payload, timeout=10)
        response_json = subject.json()

        # get the id of the default subject group
        url_7 =  url +'/subjectgroups/?group_name=Subjects'
        response = requests.get(url_7, headers=hdr, timeout=20)
        response_json = response.json()
        subject_default= response_json['data'][0]['id']

        #delete from default subject group
        url_8 = url + 'subjectgroup/' + subject_default + '/subjects'
        _ = requests.delete(url_8, headers=hdr,json=payload, timeout=10)
        #print("post?", response_json)    
      
        #post observation 
        post_observation(subject_id, "", formatted_time, hdr)


        print("\nsubject id: " + subject_id)
        print("source id: " + source_2['data'][0]['id'])
        print("sensor " + str(sen[i]) + " is uploaded to sagebrush\n")
