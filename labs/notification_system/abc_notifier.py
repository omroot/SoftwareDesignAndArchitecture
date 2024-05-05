import json
import argparse
from abc import ABC, abstractmethod

class Notifier(ABC):
    def __init__(self, name):
        self.name = name
        self.last_notification = None

    @abstractmethod
    def send(self, message: str) -> None:
        pass

    def handle_notification(self, message: str):
        self.last_notification = f"{self.name} notification: {message}"
        print(self.last_notification)

class EmailNotifier(Notifier):
    def __init__(self):
        super().__init__("Email")

    def send(self, message: str) -> None:
        self.handle_notification(message)

class SMSNotifier(Notifier):
    def __init__(self):
        super().__init__("SMS")

    def send(self, message: str) -> None:
        self.handle_notification(message)

class AppNotifier(Notifier):
    def __init__(self):
        super().__init__("App")

    def send(self, message: str) -> None:
        self.handle_notification(message)



class NotificationManager:
    def __init__(self, notifiers:list[Notifier]):
        self.notifiers = notifiers


    def alert_all(self, message:str)->None:
        results = []
        for notifier in self.notifiers:
            notifier.send(message)
            results.append(notifier.last_notification)
        return results



def read_notification_config(config_file):
    with open(config_file, 'r') as file:
        config_data = json.load(file)
    return config_data.get('notifiers', [])
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Notification System")
    parser.add_argument('--config', default='notification_config.json', help="Path to the notification configuration file")
    args = parser.parse_args()

    notifiers_config = read_notification_config(args.config)
    notifiers = []
    for notifier_config in notifiers_config:
        if notifier_config['type'] == 'email':
            notifiers.append(EmailNotifier())
        elif notifier_config['type'] == 'sms':
            notifiers.append(SMSNotifier())
        elif notifier_config['type'] == 'app':
            notifiers.append(AppNotifier())

    notification_manager = NotificationManager(notifiers)

    message = "Test notification"
    results = notification_manager.alert_all(message)

    print("Results:")
    for result in results:
        print(result)