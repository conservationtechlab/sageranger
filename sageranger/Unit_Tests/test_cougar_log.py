"""Test cougar log

Usage:
    python3 Unit_Tests.test_cougar_log

This function test creating observations in
earthranger for the specifed camera.
"""

from post_cougar_log import is_target


def main():
    """Tests creating an observation in earth ranger"""

    is_target("<camera name>", "<token?", "<label>")


if __name__ == "__main__":
    main()
