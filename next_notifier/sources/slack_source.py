from notification_source import NotificationSource
from notification import Notification
import requests
import os
from datetime import datetime
class SlackSource(NotificationSource):
    def __init__(self, subscriptiopns=[]) -> None:
        self._notifications = []
        self._unread = self.fetch()

    def fetch(self) -> bool:
        headers = {
            "Authorization": os.environ["SLACK_TOKEN"]
        }
        url = "https://slack.com/api/users.conversations?types=im,mpim&exclude_archived=true&limit=999"
        data = requests.get(url, headers=headers).json()
        dm_channel_ids = [
            x["id"] for x in data["channels"]
            if (
                "is_npim" in x.keys() and x["is_mpim"] == True and x["is_archived"] == False and (datetime.fromtimestamp(int(float(x["created"]))) - datetime.now()).days < 3
            ) 
            or (
                "last_read" in x.keys() and
                (datetime.fromtimestamp(int(float(x["last_read"]))) - datetime.now()).days < 3
            ) 
        ]
        for channel_id in dm_channel_ids:
            url ="https://slack.com/api/conversations.info?channel={}".format(channel_id)
            data = requests.get(url, headers=headers).json()
            last_read = datetime.fromtimestamp(int(float(data["channel"]["last_read"])))
            if (datetime.now() - last_read).days > 3:
                print("\t\t[slack] Skipping old conversation read on {}".format(last_read))
                continue
            print("\t\t[slack] Checking channel: {} - last read: {}".format(channel_id,last_read))
            keys = data["channel"].keys()
            if "unread_count" in keys or "unread_count_display" in keys:
                if data["channel"]["unread_count"] > 0 or data["channel"]["unread_count_display"] > 0:
                    return True
            print("\t\t[slack] No unread messages in channel: {} - last read: {}".format(channel_id,last_read))
        
        print("[slack] No unread notifications")
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

