"""Tests Post Observations

Usage:
    python3 -m unit_tests.test_post_obs

This function tests posting observations
function
"""

from datetime import datetime, UTC
from post_obs import post_observation
from get_cam_location import cam_location

TOKEN = "Bearer <token>"
CAM_NAME = "<cam_name>"  # ex: "COEX100"..
LABEL = "<label>"  # ex: "cougar", "bobcat"...


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
    current_time = datetime.now(UTC)
    formatted_time = current_time.strftime('%Y-%m-%dT%H:%M:%S.%f') + 'Z'

    _, sub_id = cam_location(CAM_NAME, TOKEN)
    post_observation(sub_id, LABEL, formatted_time, hdr)


if __name__ == "__main__":
    main()
