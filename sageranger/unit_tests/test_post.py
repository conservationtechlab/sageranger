"""Tests post event

Usage:
    python3 -m unit_tests.test_post

This function tests posting an event
on earthranger. Make sure to test from
the sageranger root folder.
"""

from post_event_er import post_event

LABEL = "<animal>"
CAMERA = "<camera_name>"
TOKEN = "Bearer <token>"


def main():
    """Tests creating an event

    This function uses global variables to
    call the post_event function and it
    prints the event id.

    """
    try:
        event_id = post_event(LABEL,CAMERA, TOKEN)
        print("Post successful Event_ID:", event_id)
        
    except KeyError:
        print("Key Error invalid authorization.")
    except IndexError:
        print("Index Error incorrect or nonexistent camera name.")

if __name__ == "__main__":
    main()
