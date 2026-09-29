"""Tests Post Monthly

Usage:
    python3 -m unit_tests.test_post_monthly

This function tests posting observations
on earthranger monthly to keep cameras
on the map.
"""

from post_monthly import post_monthly_obs
TOKEN = "Bearer <token>"
LIST_CAM = {'<list of cameras>'}  # expected formatt {'sf_id: '<camera name>'}


def main():
    """Tests creating an event

    This function uses global variables to
    call the post_montly_obs function. The
    function prints the https
    request response.

    """

    try:
        post_monthly_obs(TOKEN, LIST_CAM)
    except KeyError:
        print("Invalid Authorization.")
    except IndexError:
        print("Incorrect Camera names.")
    except AttributeError:
        print("Incorrect value type expected a dictionary type.")


if __name__ == "__main__":
    main()
