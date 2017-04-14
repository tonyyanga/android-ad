import sys
import time

from identity import experiment_identities
sys.path.append("../../appium_exec")
from run_experiment import run_experiment
from abstract_experiment import abstract_experiment


APP_DIR = "/var/www/html/mitm/Pregnancy Care Diet Nutrition_v2.2_apkpure.com.apk"


class run_weather_channel(abstract_experiment):

    def __init__(self, driver):
        self.driver = driver
        self.identities = experiment_identities()

    def experiment(self):
        time.sleep(1)
        buttons = self.driver.find_elements_by_class_name(
            "android.widget.TextView")
        buttons[3].click()
        time.sleep(5)

if __name__ == "__main__":
    print(run_experiment(run_weather_channel, app_dir=APP_DIR, num=50000))
    print(run_experiment(run_weather_channel, app_dir=APP_DIR, num=50000))
    print(run_experiment(run_weather_channel, app_dir=APP_DIR, num=50000))
    print(run_experiment(run_weather_channel, app_dir=APP_DIR, num=50000))
    print(run_experiment(run_weather_channel, app_dir=APP_DIR, num=50000))
