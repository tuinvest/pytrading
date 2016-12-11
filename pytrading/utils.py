import logging
from functools import partial

logger = logging.getLogger(__name__)


def fail_with_mode(mode, error_message, error_class):
    if mode == 'graceful':
        logger.error(error_message)
    else:
        raise error_class(error_message)


def create_fail_method(mode):
    return partial(fail_with_mode, mode)
