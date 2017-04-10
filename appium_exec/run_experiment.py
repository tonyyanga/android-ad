from appium import webdriver
import time
import subprocess
import os
import binascii

PLATFORM_NAME = "Android"


def get_driver(device_name, app_dir, appium_url='http://localhost:4723/wd/hub'):
    # generate options to match test device
    desired_caps = {}
    desired_caps['platformName'] = PLATFORM_NAME
    desired_caps['deviceName'] = device_name
    desired_caps['app'] = app_dir
    desired_caps['newCommandTimeout'] = 1200
    #desired_caps["noReset"] = True

    print(desired_caps)
    print("Getting appium_exec driver based on above options")

    driver = webdriver.Remote(appium_url, desired_caps)

    return driver


def generate_new_identity(driver):
    # TODO: use primal's hooked Android OS?

    # Generate new Android Advertising ID
    bash_cmd = """busybox sed -i -E 's/-.{12}</-%s</g' /data/data/com.google.android.gms/shared_prefs/adid_settings.xml""" % binascii.b2a_hex(
        os.urandom(6))
    cmd = ["/home/tonyyang/Android/Sdk/platform-tools/adb", "shell",
           'su -c "%s"' % bash_cmd]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()


def run_experiment(body, app_dir, num, device_name="TA00403PV1", appium_url='http://localhost:4723/wd/hub'):
    """ body - a class inheriting abstract_experiment """
    print("Start to run experiment for %i times" % num)

    # Get driver to be reused
    driver = get_driver(device_name, app_dir, appium_url)
    expr = body(driver)
    result = []

    for _ in range(num):
        generate_new_identity(driver)
        start_time = time.time()
        driver.reset()
        treatment_log = expr.treatment()
        experiment_log = expr.experiment()
        driver.close_app()
        end_time = time.time()
        result.append((start_time, end_time, treatment_log, experiment_log))
        expr.cleanup()

    driver.quit()
    return result
