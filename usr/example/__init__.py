

class TestCase(object):

    def __init__(self):
        pass

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, *args, **kwargs):
        self.teardown()

    def setup(self):
        """Hook method for setting up the test fixture before exercising it."""
        pass

    def teardown(self):
        """Hook method for deconstructing the test fixture after testing it."""
        pass

    def assertEqual(self, first, second, msg=None):
        assert first == second, self.__format_message(msg, '{} is not {}'.format(first, second))

    def __format_message(self, msg, stdmsg):
        return '{} : {}'.format(msg, stdmsg)


