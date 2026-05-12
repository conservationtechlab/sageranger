"""Tests Attach Images

Usage:
    python3 -m UnitTests.test_post

This function tests posting an event 
on earthranger. Make sure to test from
the sageranger root folder.
"""

from post_event_er import post_event

LABEL = "<animal>"
CAMERA = "<Camera name>"
TOKEN = "<bearer token>"

def main():
    """Tests creating an event"""

    event_id = post_event("<label>","<cam name>", "<token>")
    print("Event_ID:", event_id)


if __name__ == "__main__":
    main()
