'''main function
This function allows users to scrape weather data from sensors on hobolink
and posts the data to earthranger under the selected weather sensor.

This script depends on scripts in this module, including
post_weather_obs.py and config/hobotoer.yml

One must configure their individual hobotoer.yml to fit their needs by ensuring
the hobolink username, password, earthranger token, authorization and weather
sensor ID as a source on earth ranger are included correctedly.

'''
import argparse
import time
import schedule
import yaml
from post_weather_obs import hobotoer

# Parse arguments
PARSER = argparse.ArgumentParser()
PARSER.add_argument('config', type=str, help='Path to config file')
ARGS = PARSER.parse_args()
CONFIG_FILE = ARGS.config
# Load Configuration Settings from YML file
with open(CONFIG_FILE, 'r', encoding='utf-8') as stream:
    CONFIG = yaml.safe_load(stream)

USERNAME = CONFIG['username']
PASSWORD = CONFIG['password']
TOKEN = CONFIG['token']
AUTH = CONFIG['authorization']
SOURCE = CONFIG['source_id']


def main():
    ''''Runs main program and schedules future runs'''
    hobotoer(USERNAME, PASSWORD, TOKEN, AUTH, SOURCE)
    schedule.every(10).minutes.do(hobotoer,
                                  USERNAME, PASSWORD, TOKEN, AUTH, SOURCE)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
