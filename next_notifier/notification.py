class Notification:
    def __init__(self, app_identifier, message=""):
        self._app_identifier = app_identifier
        self._message = message
        if ("slack" in app_identifier):
            self._app_identifier = "slack"
        if ("whatsapp" in app_identifier):
            self._app_identifier = "whatsapp"

    @property
    def app_identifier(self):
        return self._app_identifier

    @property
    def app_name(self):
        return self._app_name 

    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self, message):
        self._message = message

    @app_identifier.setter
    def app_identifier(self, app_identifier):
        self._app_identifier = app_identifier

    def __str__(self):
        return "{} {}".format(self.app_identifier, self.message)
