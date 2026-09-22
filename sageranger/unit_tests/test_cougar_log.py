"""Test cougar log

Usage:
    python3 -m unit_tests.test_cougar_log

This function test creating observations in
earthranger for the specifed camera.
"""

from post_cougar_log import is_target

CAMERA = "<camera name>"
TOKEN = "Bearer <token>"
LABEL = "<animal>"  # ex. cougar, bobcat


def main():
    """Tests creating an observation in earth ranger

    This function uses global variables to call the is_
    target function. This function has no return
    or print statement. To verify results check for
    historical data under the selected camera icon
    in earthranger.

    """
    try:
        is_target(CAMERA, TOKEN, LABEL)
        print("Success, observation posted!")
    except KeyError:
        print("Invalid Authorization.")
    except IndexError:
        print("Incorrect or nonexistent camera name.")


if __name__ == "__main__":
    main()
