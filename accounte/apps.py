from django.apps import AppConfig


class AccounteConfig(AppConfig):
    name = 'accounte'

    def ready(self):
        import accounte

