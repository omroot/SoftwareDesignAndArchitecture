import json
import argparse
from typing import Protocol
from typing_extensions import runtime_checkable
@runtime_checkable
class Notifier(Protocol):
    name: str
    last_notification: str

    def send(self, message: str) -> None:
        pass

class EmailNotifier:
    def __init__(self):
        self.name = "Email"
        self.last_notification = None

    def send(self, message: str) -> None:
        self.last_notification = f"{self.name} notification: {message}"
        print(self.last_notification)

class SMSNotifier:
    def __init__(self):
        self.name = "SMS"
        self.last_notification = None

    def send(self, message: str) -> None:
        self.last_notification = f"{self.name} notification: {message}"
        print(self.last_notification)

class AppNotifier:
    def __init__(self):
        self.name = "App"
        self.last_notification = None

    def send(self, message: str) -> None:
        self.last_notification = f"{self.name} notification: {message}"
        print(self.last_notification)



class NotificationManager:
    def __init__(self, notifiers: list[Notifier]):
        self.notifiers = notifiers

    def run_notifier(self, notifier: Notifier, message: str) -> None:
        notifier.send(message)
    def alert_all(self, message: str) -> list[str]:
        results = []
        for notifier in self.notifiers:
            self.run_notifier(notifier, message)
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
