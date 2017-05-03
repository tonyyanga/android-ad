import json
import sys
import random

sys.path.append("../../appium_exec")
from abstract_experiment import abstract_identity_iterator
from run_experiment import generate_random_adid, generate_random_android_id

FILE_DIR = ("id_not_treated.json", "id_treated.json")
OUTPUT_FILE_DIR = ("id_permutation.json")

GROUP_SIZE = 5000


def create_permutation():
    """Create a random permutation of device identity records from files in FILE_DIR,
    and write output to OUTPUT_FILE_DIR.

    Only the first GROUP_SIZE records are loaded from each input file.
    """
    data = []
    for dir in FILE_DIR:
        with open(dir, 'r') as f:
            data += json.load(f)[:GROUP_SIZE]

    random.shuffle(data)

    with open(OUTPUT_FILE_DIR, 'w') as f:
        json.dump(data, f)
