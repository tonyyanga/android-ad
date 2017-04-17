import sys
import time

from identity import experiment_identities
sys.path.append("../../appium_exec")
from run_experiment import run_experiment
from abstract_experiment import abstract_experiment

# weather channel
APP_DIR = "/var/www/html/mitm/com.weather.Weather-5.5.6-505060343-minAPI14.apk"


class run_weather_channel(abstract_experiment):

    def __init__(self, driver):
        self.driver = driver
        self.identities = experiment_identities()

    def experiment(self):
        time.sleep(13)

if __name__ == "__main__":
    print(run_experiment(run_weather_channel, app_dir=APP_DIR, num=2500-271-517))
