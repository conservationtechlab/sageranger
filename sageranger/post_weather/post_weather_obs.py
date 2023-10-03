'''post_weather_obs
This module defines a function called hobotoer that scrapes weather
created by a sensor on hobolink and posts the data on earthranger
using api
'''

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests


def hobotoer(username, password, token, auth, source_id):
    '''hobotoer
    Tis function gets weather sensor data from hobolink and posts
    it to a source in earth ranger.

    Args:
    username: the username required to login to the sensor on hobolink,
        defined in config yml
    password: the password required to login to the sensor on hobolink,
        defined in config yml
    token: unique token for ER to authenticate http request, defined in
        config yml
        https://<YOUR INSTANCE>.pamdas.org/api/v1.0/docs/interactive/
    authorization: the other auth token for ER as defined in config
        yml, this was retrieved from the interactive api on ER
    source_id: the id of the weather sensor as a source on earth ranger
    Returns: the http request response code to tell us if the call worked
    or not
    '''

    driver = webdriver.Chrome()
    driver.get('https://www.hobolink.com/users/8034/devices/106187')

    driver.find_element("id", "login-form:j_idt34").send_keys(username)
# find password input field and insert password as well
    driver.find_element("name", "login-form:j_idt36").send_keys(password)
# click login button
    driver.find_element("name", "login-form:j_idt38").click()

    WebDriverWait(driver=driver, timeout=100).until(
        lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    error_message = "Incorrect username or password."
# get the errors (if there are)
    errors = driver.find_elements("css selector", ".flash-error")
# print the errors optionally
# for e in errors:
#     print(e.text)
# if we find that error message within errors, then login is failed
    if any(error_message in e.text for e in errors):
        print("[!] Login failed")
    else:
        print("[+] Login successful")

    driver.get('https://www.hobolink.com/users/8034/devices/106187')

    content = driver.page_source
    soup = BeautifulSoup(content)

    items = [
        item.get_text(strip=True)
        for item in soup.find_all(class_="latest-conditions-info-reading")
    ]

    print(items)

    temp = items[0]
    relative_humidity = items[1]
    dew_point = items[2]
    wind_speed = items[3]
    gust_speed = items[4]
    wind_direction = items[5]
    solar_radiation = items[6]
    rain = items[7]

    headers = {
            'X-CSRFToken': token,
            'Authorization': auth
            }

    current_time = datetime.utcnow()
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    url = 'https://sagebrush.pamdas.org/api/v1.0/observations/'

    payload = {
        "location": {
            "longitude": 0,
            "latitude": 0},
        "recorded_at": formatted_time,
        "source": source_id,
        "device_status_properties": [
            {"value": temp,
             "label": "temperature",
             "units": "C"
             },
            {"value": relative_humidity,
             "label": "relative_humidity",
             "units": "%"
             },
            {"value": dew_point,
             "label": "dew_point",
             "units": "C"
             },
            {"value": wind_speed,
             "label": "wind_speed",
             "units": "m/s"
             },
            {"value": gust_speed,
             "label": "gust_speed",
             "units": "m/s"
             },
            {"value": wind_direction,
             "label": "wind_direction",
             "units": "degrees"
             },
            {"value": solar_radiation,
             "label": "solar_radiation",
             "units": "W/m^2"
             },
            {"value": rain,
             "label": "rain",
             "units": "mm"
             }
        ],
        "additional": {
            "temperature": temp,
            "relative_humidity": relative_humidity,
            "dew_point": dew_point,
            "wind_speed": wind_speed,
            "gust_speed": gust_speed,
            "wind_direction": wind_direction,
            "solar_radiation": solar_radiation,
            "rain": rain
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=10)
    resp = response.json()
    print(resp)
    return resp
