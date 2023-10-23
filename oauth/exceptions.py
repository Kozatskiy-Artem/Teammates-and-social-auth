class OAuth2Exception(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message
        super().__init__(self.message)
