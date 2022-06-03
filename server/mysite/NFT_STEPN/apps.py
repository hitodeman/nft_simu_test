from django.apps import AppConfig


class NftStepnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'NFT_STEPN'

    def ready(self):
        from .logic.ap_scheduler import start
        print('定期実行起動確認')
        start()