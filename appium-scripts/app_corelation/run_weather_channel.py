import sys
import time
import argparse
import json

from identity import experiment_identities
sys.path.append("../../appium_exec")
from run_experiment import run_experiment
from abstract_experiment import abstract_experiment

# weather channel
APP_DIR = "/var/www/html/mitm/com.weather.Weather-5.5.6-505060343-minAPI14.apk"


class run_weather_channel(abstract_experiment):

    def __init__(self, driver):
        self.driver = driver
        self.identities = experiment_identities()  # set start index here

    def experiment(self):
        time.sleep(11)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--log-dir", required=True, help="Where experiment log is be stored")
    args = parser.parse_args()

    result = run_experiment(run_weather_channel,
                            app_dir=APP_DIR, num=7500)

    with open(args.log_dir, 'a') as f:
        json.dump(result, f)
