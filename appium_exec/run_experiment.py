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


def generate_new_identity(driver, device_name, identities=None):
    # TODO: use primal's hooked Android OS?

    # Generate new Android Advertising ID
    adid, android_id = "", ""
    if identities:
        adid, android_id, group_id = identities.next()
    else:
        adid = generate_random_adid()
        android_id = generate_random_android_id()

    # Reset Android ID and ad id
    bash_cmd1 = """busybox sed -i -E 's/.{8}-.{4}-.{4}-.{4}-.{12}</%s</g' /data/data/com.google.android.gms/shared_prefs/adid_settings.xml""" % adid

    bash_cmd2 = "settings put secure android_id %s" % android_id
    cmd = ["/home/tonyyang/Android/Sdk/platform-tools/adb", "-s", device_name, "shell",
           'su -c "%s;%s"' % (bash_cmd1, bash_cmd2)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
    buf = p.read()
    p.close()
    return group_id


def generate_random_adid():
    return binascii.b2a_hex(os.urandom(4)) + '-' + \
        binascii.b2a_hex(os.urandom(2)) + '-' + \
        binascii.b2a_hex(os.urandom(2)) + '-' + \
        binascii.b2a_hex(os.urandom(2)) + '-' + \
        binascii.b2a_hex(os.urandom(6))


def generate_random_android_id():
    return binascii.b2a_hex(os.urandom(8))


def run_experiment(body, app_dir, num, device_name="TA00403PV1", appium_url='http://localhost:4723/wd/hub'):
    """ body - a class inheriting abstract_experiment """
    print("Start to run experiment for %i times" % num)

    # Get driver to be reused
    driver = get_driver(device_name, app_dir, appium_url)
    expr = body(driver)
    result = []

    try:
        for i in range(num):
            print("Experiment" + str(i))
            group_id = generate_new_identity(
                driver, device_name, expr.identities)
            start_time = time.time()
            try:
                driver.reset()
            except Exception:
                print("reset exception occurred")
            time.sleep(1)
            driver.reset()
            treatment_log = expr.treatment()
            experiment_log = expr.experiment()
            driver.close_app()
            end_time = time.time()
            result.append((group_id, start_time, end_time,
                           treatment_log, experiment_log))
            expr.cleanup()
            driver.quit()
    finally:
        return result
