"""Unpack Info

This module contains the logice for
unpacking the config file. It maps
all the values from the config file
to the corressponding values in the
data class sensor_info. These functions
are used in post_camera_er and in the repo
cougarvision.

"""
import argparse
from dataclasses import fields
import yaml


def parse_args():
    """Creates parser for config yaml.

    This function creates an arguement parser that creates an
    args container with the arguement 'CONFIG'.

    Returns:
        argsparse.Namespace: An object containing all parsed arguement
            values as attributes (e.g., args.CONFIG).
    """
    parser = argparse.ArgumentParser(description='Retrieves information from'
                                     'config and posts events '
                                     'and observations')
    parser.add_argument('CONFIG', type=str, help='path to config file.')

    return parser.parse_args()


def get_config_info(class_type):
    """Parses through config file.

    This function maps values to the dataclasses
    found in get_info.

    Args:
        class_type (str): get info has two dataclasses
            config info and display info

    Return:
        dict: unpacked and mapped values to
            class type
    """

    args = parse_args()
    config_path = args.CONFIG

    with open(config_path, 'r', encoding='utf-8') as file:
        config_dict = yaml.safe_load(file)

    # for direct mapping only use fields in the class fields
    valid_keys = {f.name for f in fields(class_type)}
    filtered_keys = {k: v for k, v in config_dict.items() if k in valid_keys}

    return class_type(**filtered_keys)
