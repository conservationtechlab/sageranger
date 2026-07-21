"""Sensor Info

This class holds the values from
the config file. Unpack_info
handles the logic of mapping the
variables to their values.
"""

from dataclasses import dataclass


@dataclass
class SensorInfo:
    # pylint: disable=too-many-instance-attributes
    """SensorInfo

    This dataclass declares the
    config datatypes. The variable
    names must match those in the
    config file.
    """

    path_csv: str
    auth_token: str
    source_type: str
    provider: str
    subject_subtype: str
    subject_type: str
    content_type: str
    source_type: str
    group_name: str
    sensor_type: bool
