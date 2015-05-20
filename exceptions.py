class CinderClientBaseException(Exception):
    def __init__(self, message):
        self.message = message


class ServerNotFound(CinderClientBaseException):
    def __init__(self, message):
        self.message = message


class VolumeNotFound(CinderClientBaseException):
    def __init__(self, message):
        self.message = message


class MultipleServersFound(CinderClientBaseException):
    def __init__(self, message):
        self.message = message


class MultipleVolumesFound(CinderClientBaseException):
    def __init__(self, message):
        self.message = message
