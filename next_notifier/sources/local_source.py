from notification_source import NotificationSource
from notification import Notification

import sqlite3
import subprocess

userpath = subprocess.check_output(["getconf", "DARWIN_USER_DIR"]).decode("utf-8").strip()

dbpath = "{}com.apple.notificationcenter/db2/db".format(userpath)

sql = "select a.identifier from record r join app a on r.app_id = a.app_id;"

class LocalSource(NotificationSource):
    def __init__(self, subscriptions=[]) -> None:
        self._notifications = []
        self._subscriptions = subscriptions
        self._unread = self.fetch()

    def fetch(self) -> None:
        con = sqlite3.connect(dbpath)
        cur = con.cursor()
        self._notifications = [
            Notification(notif[0]) for notif in cur.execute(sql) 
        ]
        con.close()
        for n in self._notifications:
            print("-> {}".format(n.app_identifier))
        return len(self._notifications) > 0
        
    @property
    def notifications(self) -> Notification:
        return self._notifications
    
    @property
    def unread(self) -> bool:
        return self._unread

    @property
    def subscriptions(self):
        return self._subscriptions

    
