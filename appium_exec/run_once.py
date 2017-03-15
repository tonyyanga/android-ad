from appium import webdriver

PLATFORM_NAME = "Android"


def get_driver(device_name, app_dir, appium_url='http://localhost:4723/wd/hub'):
    # generate options to match test device
    desired_caps = {}
    desired_caps['platformName'] = PLATFORM_NAME
    desired_caps['deviceName'] = device_name
    desired_caps['app'] = app_dir
    desired_caps['newCommandTimeout'] = 1200

    print(desired_caps)
    print("Getting appium_exec driver based on above options")

    driver = webdriver.Remote(appium_url, desired_caps)

    return driver


def run_once(body, app_dir, device_name="TA00403PV1", appium_url='http://localhost:4723/wd/hub'):
    """ body - a function that takes in a webdriver.driver
    """
    print("Start to run once")
    driver = get_driver(device_name, app_dir, appium_url)
    body(driver)
    print("Finish running once")
    driver.quit()
