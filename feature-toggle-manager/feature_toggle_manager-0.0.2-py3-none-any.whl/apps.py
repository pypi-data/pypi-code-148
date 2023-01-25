from django.apps import AppConfig


class FeatureToggleManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feature_toggle_manager"

    def ready(self) -> None:
        import feature_toggle_manager.signals
