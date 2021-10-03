from enum import Enum


class LogType(Enum):
    CONSOLE = 1


class LogLevel(Enum):
    VERBOSE = 1
    DEBUG = 2
    INFO = 3
    WARNING = 4
    CRITICAL = 5
    NONRECOVERALE = 6


class CommonAppFramework:
    """
    A placeholder for any functions that should be shared between all the applications
    """

    def __init__(self):
        self.log_output = {}
        # set debug logging options
        self.log_output[LogType.CONSOLE] = True
        # .. whatever we don't log, set to false
        for level in LogLevel:
            if not level in self.log_output:
                self.log_output[level] = False
        self.log_level = LogLevel.VERBOSE
        # log that we are starting up
        self.log("Starting {}".format(self.__class__.__name__))

    def log(self, content="default log message", log_level=LogLevel.VERBOSE):
        """
        Central logging function for an application.
        'content' can be anything at all, and is formatted into a string via pprint.
        'log_level' needs to be a valud from the LogLevel enum
        CommonAppFramework.log_output is an array (True|False)
          that determine which output streams log output goes to.
        """
        # if the event isn't a high enough level to be logged, ignore it
        if log_level.value < self.log_level.value:
            return
        # otherwise, lets generate a nice human readable log string
        from pprint import pformat

        as_string = "{} {}".format(log_level.name, pformat(content))
        # for each log type, check if enabled, and if so take action
        if self.log_output[LogType.CONSOLE]:
            print(as_string)

    def run(self):
        pass
