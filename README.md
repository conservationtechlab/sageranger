# sageranger
A package to aide in the utilization of Earthranger as a way to capture and display data of interest from camera traps and other data loggers. This package is used in cougarvision to post events and observations: https://github.com/conservationtechlab/cougarvision/blob/master/README.md

Installation:
```
pip install sageranger
```
# Additional setup
For use in cougarvision (visit readme) or for testing (see below). An authorization token is needed "Bearer <token>" visit <your_instance>.pamdas.org/admin. Under Das Configuration in DAS Tokens add a new Das Acess Token. Set the expiration date and ensure the scope is 'read write'. We recommend the use of an online UUID generator to create a unique token. Once the above fields are filled save the token. This token can be used in the fetch and alert yaml in cougarvision or for testing purposes in the unit tests. 

# Sageranger Functions
Sageranger performs multiple functions such as posting events to earthranger, attaching images to events, creating camera sources and subjects, posting observations to camera subjects and retrieving camera coordinates and subject ids. post_camera_er.py uses a .csv containing camera data such as coordinates located on its local machine and posts an intial observation for each camera as their specified coordinates. post_event_er.py posts events of specified typ(ex. "cougarvision_detection") to earhranger. post_event uses get_cam_locations.py for retrieveing camera coordinates and subject_id. post_cougar_log.py posts an observation with an animal of interest has been detected (ex. "cougar", "bobcat" ...). post_monthly.py is an optional function which posts empty observations to keep cameras visible on the earthranger map. post_obs.py is a supporting function which hands posting observations for the post_camera.py, post_monthly.py, and post_cougar_log.py functions.For more information about the earthranger api visit  <your_instance>.pamdas.org/interactive


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
test post_monthly:
```
python3 -m unit_tests.test_post_monthly
```
test post_obs.py:
```
python3 -m unit_tests.test_post_obs
```
test_post.py
```
python3 -m unit_tests.test_post
```