"""Tests camera locations

Usage:
    python3 -m UnitTests.test_locations

Make sure you are testing from the sageranger
root folder.
"""

from get_cam_location import cam_location


def main():
    """Tests get cam locations"""
    coordinates, s_id = cam_location("<cam name>", "<token>")
    print("Coordintes and ID:", coordinates, s_id)


if __name__ == "__main__":
    main()
