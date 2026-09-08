"""Create Flow

These functions work with the information provided
in post_camera_er. The config value 'red_node'determines
if these functions will be used. They currently work with
base.json and branch.json, which work for temperature sensors.

"""
import json
import copy
from importlib import resources
import uuid


def create_branch(device_name, src_id, location, token, index):
    # pylint: disable=too-many-locals
    """Creates a branch for sensor

    This function creates a branch of nodes for red node flow using
    a json template found in the observations_payloads folder.

    Args:
        device_name (str): name of sensor
        src_id (str): source id of sensor from earthranger
        location (tuple): tuple latitude and logtitude of sensor
        token (str): authorization token from earthranger
        index (int): counter to keep track of branches created

    Return:
        tuple (int, dict): this function returns the the id of
         the first node in a branch and its corresponding information
         in json formatt (or dict).
    """
    lat, long = location

    # load branch.json template for creating nodes
    path_to_json = resources.files(
                       "sageranger") / "observation_payloads" / 'branch.json'

    with path_to_json.open('r', encoding='utf-8') as file:
        data = json.load(file)

    # changes node location on red node gui
    branch_y = 380 + (index * 100)

    temp = []
    start_node = ""

    # change node ids
    id_map = {
        node["id"]: uuid.uuid4().hex[:16]
        for node in data
    }

    # create copy of json template and match ids to corresponding nodes
    for node in data:
        new_node = copy.deepcopy(node)
        old_id = new_node["id"]
        new_node["id"] = id_map[old_id]
        new_node["y"] = branch_y

        # change device name
        if new_node.get("type") == "change" and new_node.get(
                "name") == "DEVICE_NAME":
            start_node = new_node["id"]

        if "name" in new_node:
            new_node["name"] = new_node["name"].replace(
                "DEVICE_NAME",
                device_name
                )

        # ids of nodes should be mapped in each nodes wires section
        if "wires" in new_node:
            for output in new_node["wires"]:
                for i, target_id in enumerate(output):

                    if target_id in id_map:
                        output[i] = id_map[target_id]

        temp.append(new_node)

    # find template node
    template_node = next(
         node for node in temp
         if node["type"] == "template"
    )

    template = template_node["template"]

    # replaces the values we care about
    template = template.replace(
         "SOURCE_ID",
         src_id
    )

    template = template.replace(
         "LATITUDE",
         str(lat)
    )

    template = template.replace(
         "LONGITUDE",
         str(long)
    )

    template_node["template"] = template

    # find http node and replace token for actual token
    http_node = next(
        node for node in temp
        if node["type"] == "http request"
    )

    for header in http_node["headers"]:
        if header["keyValue"] == "Authorization":
            header["valueValue"] = token

    return start_node, temp


def add_switch(device_name, node_id, data):
    """Add ids to switch

    This function adds the name and id of
    the starting node in a branch to the node
    Device switch.

    Args:
        device_name (str): name of sensor
        node_id (str): id of the starting node in
            a branch
        data (dict): json formatted information from
            base.json
    """
    switch_node = next(
          node for node in data
          if node.get("name") == "Device Switch"
    )

    # Add a new rule
    switch_node["rules"].append({
        "t": "eq",
        "v": device_name,
        "vt": "str"
    })

    # Add the new output
    switch_node["outputs"] += 1

    switch_node["wires"].append([
        node_id
     ])


def create_flow(list_of_sensors, token):
    """Creates node red flow

    This function using the add_switch and create branch
    function, as well as the base.json creates a final_flow.json
    that can be imported to node red.

    Args:
        list_of_sensors (list): is a list of tuples from post_camera_er
             each tuple contains device name, id, and location
        toke (str): Authorization token from earthranger

    """
    count = 0
    branches = []

    path_to_json = resources.files(
                            "sageranger"
                            ) / "observation_payloads" / "base.json"

    with path_to_json.open('r', encoding='utf-8') as file:
        base = json.load(file)

    for sensor in list_of_sensors:
        device_name = sensor[0]
        sub_id = sensor[1]
        lat = sensor[2]
        long = sensor[3]

        start_node, new_branch = create_branch(device_name,
                                               sub_id,
                                               (lat, long),
                                               token,
                                               count
                                               )

        add_switch(device_name, start_node, base)
        branches.extend(new_branch)
        count += 1

    with open("final_flow.json", "w", encoding='utf-8') as f:
        json.dump((base + branches), f, indent=2)


