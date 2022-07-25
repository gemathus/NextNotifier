from notification_source import NotificationSource
from notification import Notification
import requests
import os
class APISource(NotificationSource):
    def __init__(self, subscriptiopns=[]) -> None:
        self._notifications = []
        self._unread = self.fetch()

    def fetch(self) -> None:
        headers = {
            "X-Auth-Token": os.environ["CHAT_TOKEN"],
            "X-User-Id": os.environ["CHAT_USER_ID"]
        }
        response = requests.get("{}/api/v1/subscriptions.get".format(os.environ["CHAT_URL"]), headers=headers)
        data = response.json()
        for item in data["update"]:
            if item["unread"] > 0:
                return True
        
        return False
        
        
    @property
    def notifications(self) -> Notification:
        return self._notifications
    
    @property
    def unread(self) -> bool:
        return self._unread
    
    @unread.setter
    def unread(self, value: bool) -> None:
        self._unread = value

