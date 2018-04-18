class ServiceError(Exception):
    """Raise for exceptions in services"""

    def __init__(self, message):
        super().__init__(message)