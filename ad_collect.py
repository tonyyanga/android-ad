import os
import sys
import argparse
import time


def user_confirm(prompt=None, resp=False):
    """prompts for yes or no response from the user. Returns True for yes and
    False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >>> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n: 
    True
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: 
    False
    >>> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    """

    if prompt is None:
        prompt = 'Confirm'

    if resp:
        prompt = '%s [%s/%s] ' % (prompt, 'Y', 'n')
    else:
        prompt = '%s [%s/%s]  ' % (prompt, 'y', 'N')

    while True:
        ans = raw_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-L", "--log-dir", required=True, help="A directory in which logs can be stored")
    parser.add_argument(
        "-S", "--appium-script", required=True, help="A script to be run")
    args = parser.parse_args()

    log_dir = args.log_dir
    if log_dir[-1:] != "/":
        log_dir += '/'

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    print("Using log directory: " + log_dir)

    print("Please execute the following command:")

    mitm_script_name = os.path.dirname(
        os.path.realpath(__file__)) + "/mitm-scripts/print_host.py"

    mitm_cmd = '"' + mitm_script_name + ' -L ' + log_dir + '"'

    print("mitmdump --socks -p 48080 -s %s" % mitm_cmd)

    if not user_confirm("Success?"):
        sys.exit(1)

    with open(log_dir + "timestamp.log", 'w') as f:
        count = 0
        print("Start running test script: " + args.appium_script)
        start = int(time.time())
        print("Start launching at " + str(start))
        execfile(args.appium_script)
        count += 1
        end = int(time.time())
        print("Finish at " + str(end))
        f.write(str(count) + '|' + str(start) + '|' + str(end))
