import functools
import inspect
from configs.logger_factory import get_logger


def log_ejecucion(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        module_name = inspect.getmodule(func).__name__
        logger = get_logger(module_name)

        logger.info(f"Iniciando: {func.__name__}")
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error en {func.__name__}: {e}")
            raise
        finally:
            logger.info(f"Finalizado: {func.__name__}")

    return wrapper
