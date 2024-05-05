import unittest
from protocol_notifier import EmailNotifier, SMSNotifier, AppNotifier
from protocol_notifier import NotificationManager, read_notification_config
class TestNotificationManager(unittest.TestCase):


    def test_notification_manager(self):
        notifiers_config = read_notification_config('notification_config.json')
        notifiers = []
        for notifier_config in notifiers_config:
            if str(notifier_config['type']).lower() == 'email':
                notifiers.append(EmailNotifier())
            elif str(notifier_config['type']).lower() == 'sms':
                notifiers.append(SMSNotifier())
            elif str(notifier_config['type']).lower() == 'app':
                notifiers.append(AppNotifier())

        notification_manager = NotificationManager(notifiers)

        message = "Test notification"
        results = notification_manager.alert_all(message)
        # Assert that each notifier's send method returns the expected message
        expected_result = [
            f"Email notification: {message}",
            f"SMS notification: {message}",
            f"App notification: {message}"
        ]
        self.assertCountEqual(results, expected_result)

if __name__ == "__main__":
    unittest.main()