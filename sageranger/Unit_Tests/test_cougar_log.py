"""Test cougar log

Usage:
    python3 Unit_Tests.test_cougar_log

This function test creating observations in
earthranger for the specifed camera.
"""

from post_cougar_log import is_target

CAMERA = "<camera name>" 
TOKEN = "<bearer token>"
LABEL = "<animal>"  # ex. cougar, bobcat

def main():
    """Tests creating an observation in earth ranger"""

    is_target(CAMERA, TOKEN, LABEL)


if __name__ == "__main__":
    main()
