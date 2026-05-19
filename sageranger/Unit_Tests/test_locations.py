"""Tests camera locations

Usage:
    python3 -m UnitTests.test_locations

Make sure you are testing from the sageranger
root folder.
"""

from get_cam_location import cam_location

CAMERA = "<camera name>"
TOKEN = "<bearer token>"


def main():
    """Tests get cam locations

    This function uses global variables to call the 
    cam_location function. This function prints the 
    coordinates and the event id.
    
    """
    coordinates, s_id = cam_location(CAMERA, TOKEN)
    print("Coordintes and ID:", coordinates, s_id)


if __name__ == "__main__":
    main()
