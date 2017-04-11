import json
import sys

sys.path.append("../../appium_exec")
from abstract_experiment import abstract_identity_iterator
from run_experiment import generate_random_adid, generate_random_android_id

FILE_DIR = "identities.json"


class experiment_identities(abstract_identity_iterator):

    def __init__(self):
        with open(FILE_DIR, 'r') as f:
            self.data = json.load(f)
        assert len(self.data) > 1
        self.index = -1

    def next(self):
        self.index += 1
        return self.data[self.index]


def reset_identities():
    data = []
    for _ in range(1000):
        data.append((generate_random_adid(), generate_random_android_id()))
    with open(FILE_DIR, 'w') as f:
        f.write(json.dumps(data))