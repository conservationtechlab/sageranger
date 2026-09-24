"""Tests camera locations

Usage:
    python3 -m unit_tests.test_locations

Make sure you are testing from the sageranger
root folder.
"""

from get_cam_location import cam_location

CAMERA = "<camera name>"
TOKEN = "Bearer <token>"


def main():
    """Tests get cam locations

    This function uses global variables to call the
    cam_location function. This function prints the
    coordinates and the event id.

    """
    try:
        coordinates, s_id = cam_location(CAMERA, TOKEN)
        print("Success Coordintes and ID:", coordinates, s_id)
    except KeyError:
        print("Invalid Authorization.")
    except IndexError:
        print("Invalid or non-existent camera name.")


if __name__ == "__main__":
    main()
