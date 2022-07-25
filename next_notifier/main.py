from sources.local_source import LocalSource
from sources.api_source import APISource
from sources.slack_source import SlackSource
from suscribers.blink import Blink
from constants.apps import APPS
subscribed = ["whatsapp", "slack", "chrome"]

blinker = Blink()
local_source = LocalSource(subscribed)

#REAL CODE
apps_with_notifications = [n.app_identifier for n in local_source.notifications]

blinker.notify(apps_with_notifications)

if "slack" not in apps_with_notifications:
    print("fetching slack from api")
    slack_source = SlackSource(subscribed)
    if slack_source.unread:
        apps_with_notifications.append("slack")        

blinker.notify(apps_with_notifications)

