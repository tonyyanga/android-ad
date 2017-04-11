class abstract_identity_iterator():
    """ an identity iterator to provide pre-defined identities"""

    def __init__(self):
        pass

    def next(self):
        """ Should return a pair (<adid>, <android_id>) """
        pass


class abstract_experiment:
    """ an experiment to be provided to run_once function"""

    identities = None

    def __init__(self, driver):
        """ accept the driver and number of experiments"""
        pass

    def treatment(self):
        """Should return a string identifier that describes the treatment 

           Expect the app is already launched
        """
        return ""

    def experiment(self):
        """Do the experiment after the treatments, return a string log"""
        raise NotImplementedError

    def cleanup(self):
        """called after every experiment to clean up

           Expect the app is already closed
        """
        pass
