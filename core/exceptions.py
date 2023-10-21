class InstanceDoesNotExistError(Exception):
    def __init__(self, message="Instance does not exists", *args, **kwargs):
        super().__init__(message, *args)
