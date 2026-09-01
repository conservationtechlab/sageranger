# sageranger
A package to aide in the utilization of Earthranger as a way to capture and display data of interest from camera traps and other data loggers. This package is used in cougarvision to post events and observations: https://github.com/conservationtechlab/cougarvision/blob/master/README.md

Installation:
```
pip install sageranger
```
# Additional Setup
For use in cougarvision (visit readme) or for testing (see below) an authorization token is needed "Bearer <token>". Visit <your_instance>.pamdas.org/admin. Under Das Configuration in DAS Tokens add a new Das Acess Token. Set the expiration date and ensure the scope is 'read write'. We recommend the use of an online UUID generator to create a unique token. Once the above fields are filled save the token. This token can be used in the fetch and alert yaml in cougarvision or for testing purposes in the unit tests. To use the 'post_camera_er' script to post sensors with their corresponding locations on earthranger, the config file 'sensor_info' must be completed with the authorization token and subject details. Addtionally a csv with camera names and coordinates must be provided see 'camera_test' in the config folder for an example of the expected format.

# sageranger Functions
Sageranger performs multiple functions such as posting events to earthranger, attaching images to events, creating camera sources and subjects, posting observations to camera subjects and retrieving camera coordinates and subject ids.

post_camera_er.py:
Uses a csv containing camera data such as coordinates and camera names. This csv is located on your local machine. Post camera posts an intial observation for each camera at their specified coordinates to make cameras visible on the map.

post_event_er.py:
Posts events of specified type (ex. "cougarvision_detection") to earthranger. 

attach_image_er.py:
Attaches an image to an event given an image and event id.

get_cam_locations.py:
Retrieves the coordinates and subject_id of the cameras.

post_cougar_log.py:
posts an observation with an animal of interest has been detected (ex. "cougar", "bobcat" ...).

post_monthly.py:
An optional function which posts empty observations to keep cameras visible on the earthranger map.

post_obs.py:
Is a supporting function which handles posting observations for the post_camera.py, post_monthly.py, and post_cougar_log.py functions. 

For more information about the earthranger api visit  <your_instance>.pamdas.org/api/v1.0/docs/interactive/

# Testing
The sageranger files are not directly runnable but each have their own test case. All of these test cases are located in the unit_tests folder. These test cases require an authorization token as well as additional information such as camera_name, label...etc see test docstrings for more information.

test_cougar_log.py:
```
python3 unit_tests.test_cougar_log
```
test_attach.py:
```
python3 -m unit_tests.test_attach
```
test_locations.py:
```
python3 -m unit_tests.test_locations
```
test_post_monthly:
```
python3 -m unit_tests.test_post_monthly
```
test_post_obs.py:
```
python3 -m unit_tests.test_post_obs
```
test_post.py
```
python3 -m unit_tests.test_post
```