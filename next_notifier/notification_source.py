from abc import ABC, abstractmethod, abstractproperty
from notification import Notification

class NotificationSource(ABC):
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def fetch(self) -> Notification:
        pass

    @abstractproperty
    def notifications(self) -> Notification:
        pass