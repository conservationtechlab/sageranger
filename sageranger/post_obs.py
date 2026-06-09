import requests

def post_observation(subject_id, label, time, hdr):
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
    
