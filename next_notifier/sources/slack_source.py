from notification_source import NotificationSource
from notification import Notification
import requests
import os
class SlackSource(NotificationSource):
    def __init__(self, subscriptiopns=[]) -> None:
        self._notifications = []
        self._unread = self.fetch()

    def fetch(self) -> None:
        headers = {
            "Authorization": os.environ["SLACK_TOKEN"]
        }
        url = "https://slack.com/api/users.conversations?types=im,mpim&exclude_archived=true&limit=999"
        data = requests.get(url, headers=headers).json()
        dm_channel_ids = [x["id"] for x in data["channels"]]
        for channel_id in dm_channel_ids:
            url ="https://slack.com/api/conversations.info?channel={}".format(channel_id)
            data = requests.get(url, headers=headers).json()
            keys = data["channel"].keys()
            if "unread_count" in keys or "unread_count_display" in keys:
                if data["channel"]["unread_count"] > 0 or data["channel"]["unread_count_display"] > 0:
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

