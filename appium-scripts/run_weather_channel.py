
import sys
sys.path.append("../appium_exec")
from appium_exec.run_once import run_once


APP_DIR = "/var/www/html/mitm/com.weather.Weather-5.5.6-505060343-minAPI14.apk"


def body(driver):

    # driver.launch_app()
    time.sleep(10)
    driver.close_app()


run_once(body, app_dir=APP_DIR)
