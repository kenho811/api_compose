__all__ = ["get_logger"]

from api_compose.core.logging.adapter import LoggerAdapter
from api_compose.core.settings.settings import GlobalSettingsModelSingleton


def get_logger(
        name: str,
        overwrite=True,
) -> LoggerAdapter:
    log_file_path = GlobalSettingsModelSingleton.get().logging.log_file_path
    logging_level = GlobalSettingsModelSingleton.get().logging.logging_level
    log_format = GlobalSettingsModelSingleton.get().logging.log_format
    return LoggerAdapter(
        name=name,
        log_file_path=log_file_path,
        overwrite=overwrite,
        logging_level=logging_level,
        log_format=log_format
    )
