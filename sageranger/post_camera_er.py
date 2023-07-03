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
    camera: a list of all the names of the new camera traps that need to be
    uploaded to Earthranger
    cord: a list of all the coordinates of the new camera traps that need to
    be uploaded to Earthranger, in the form of [latitude,longitude]
    token: unique token for ER to authenticate http request, defined in config yml
    authorization: the other auth token for ER as defined in config yml, this was
    retrieved from the interactive api on ER
    https://<YOUR INSTANCE>.pamdas.org/api/v1.0/docs/interactive/
        
    Returns: the two unique ids of the camera trap as subject and source on Earthranger 
    '''

    headers = {
        'X-CSRFToken': token,
        'Authorization':auth,
        'Accept':'application/json'
    }


    #sample camera trap sets and coordinates as two lists, used as an example here
    cam= 'S014', 'S018', 'S019', 'S045'
    cord= [[112, 32], [112.00001, 32.00001], [112.00002, 32.00002], [112.00003, 32.00002]]

    url_source = 'https://sagebrush.pamdas.org/api/v1.0/sources/'
    url_subject = 'https://sagebrush.pamdas.org/api/v1.0/subjects/'


    #start loop
    for i in enumerate(cord):
        i = i[0]
        current_time = datetime.utcnow()
        formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'
 
        #post subject
        subject = {
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
                    "coordinates": [cord[i][0],cord[i][1]]}}
        }

        response_subject = requests.post(url_subject, headers=headers, json=subject, timeout=10)
        subject_js = response_subject.json()
        subject_id = subject_js['data']['id']
        print(response_subject)
        print("\nsubject id: " + subject_id)

        #post_source
        source = {
            "source_type": "seismic",
            "manufacturer_id": cam[i],
            "model_name": cam[i],
            "additional": {},
            "provider": "cougar_vision",
            "subject": subject_id,
            "assigned_range": {}
        }

        response_source = requests.post(url_source, headers=headers, json=source, timeout=10)
        response_js=response_source.json()
        source_id = response_js['data']['id']

        #link source to subject
        source = {
            "source_type": "seismic",
            "manufacturer_id": cam[i],
            "model_name": cam[i],
            "additional": {},
            "provider": "cougar_vision",
            "source" : source_id,
            "subject": subject_id,
            "assigned_range": {}
        }

        url_link = 'https://sagebrush.pamdas.org/api/v1.0/subject/'+subject_id+'/sources/'
        response_link = requests.post(url_link, headers=headers, json=source, timeout=10)
        print(response_link)
        print('\ncamera trap ' + cam[i] + ' is uploaded to sage brush\n')

        #return source id
        response_3 = requests.get(url_link, headers=headers, timeout=10)
        res3=response_3.json()
        print('source id: '+res3['data']['id']+'\n')

        #post observations at the camera trap
        #url_obs = "https://sagebrush.pamdas.org/api/v1.0/observations/"
        #observation = {"location": {"longitude": 0, "latitude": 0},
            #"recorded_at": formatted_time,
            #"source": source_id,
            #"device_status_properties": [{"value": label, "label": "animal", "units": ""}],
            #"additional": {"animal": label}}
        #requests.post(url_obs, headers=Headers, json=observation)
