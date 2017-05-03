import json
import sys

sys.path.append("../../appium_exec")
from abstract_experiment import abstract_identity_iterator
from run_experiment import generate_random_adid, generate_random_android_id

FILE_DIR = "id_permutation.json"

GENERATE_NUMBER = 20000


class experiment_identities(abstract_identity_iterator):

    """A device identity iterator based on the json config at FILE_DIR"""

    def __init__(self, start_index=0):
        with open(FILE_DIR, 'r') as f:
            self.data = json.load(f)
        assert len(self.data) > 1
        self.index = start_index

    def next(self):
        self.index += 1
        return self.data[self.index]


def find_index(adid_segment):
    """Among all records in the json config, find the index of one that
       contains the same Android Ad id"""
    with open(FILE_DIR, 'r') as f:
        data = json.load(f)
    for i in range(len(data)):
        if adid_segment in data[i][0]:
            print i
            break


def reset_identities(group_id=0):
    """Generate a json config at FILE_DIR with GENERATE_NUMBER records

    The json config is a JSON list of [<Android ID>, <Android Advertising ID>, <Group number>]
    """
    data = []
    for _ in range(GENERATE_NUMBER):
        data.append((generate_random_adid(),
                     generate_random_android_id(), group_id))
    with open(FILE_DIR, 'w') as f:
        json.dump(data, f)
