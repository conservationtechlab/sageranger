"""Tests Post Observations

Usage:
    python3 -m unit_tests.test_post_obs

This function tests posting observations
function
"""

import datetime
from post_obs import post_observation
from get_cam_location import cam_location

TOKEN = "Bearer <token>"
CAM_NAME = "<camera name>"  # ex: "COEX 100"..
LABEL = "<animal>"  # ex: "cougar", "bobcat"...


def main():
    """Tests creating an event

    This function uses global variables to
    call the cam location function for
    subject_id and post observation which
    prints the https request response.

    """
    hdr = {
        'Authorization': TOKEN,
        'Accept': 'application/json'
    }
    # set up for test
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f')

    try:
        _, sub_id = cam_location(CAM_NAME, TOKEN)
        post_observation(sub_id, LABEL, formatted_time, hdr)

    except KeyError:
        print("Invalid Authorization.")


if __name__ == "__main__":
    main()
