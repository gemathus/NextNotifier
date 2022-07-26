from sources.local_source import LocalSource
from sources.api_source import APISource
from sources.slack_source import SlackSource
from suscribers.blink import Blink
from constants.apps import APPS
from dotenv import load_dotenv
load_dotenv()

subscribed = ["whatsapp", "slack", "chrome"]

blinker = Blink()
local_source = LocalSource(subscribed)

#REAL CODE
apps_with_notifications = []
[apps_with_notifications.append(n.app_identifier) for n in local_source.notifications if n.app_identifier not in apps_with_notifications]
print("[sys] Local notifications: {}".format(len(apps_with_notifications)))
blinker.notify(apps_with_notifications)

if "slack" in apps_with_notifications:
    print("[sys] Fetching slack from API")
    slack_source = SlackSource(subscribed)
    new_apps = []
    if slack_source.unread == False:
        print("[sys] No unread notifications in Slack")
        new_apps = [a for a in apps_with_notifications if "slack" not in a]
        print("Notifications: ", new_apps)

    print("[sys] Executing blinker")
    blinker.notify(new_apps)

