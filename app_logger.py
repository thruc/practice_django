from logging import getLogger
import logging.config
import logging.handlers
import pathlib
import inspect



logging = getLogger(__name__)

# MESSAGE_FORMAT
FUNC_STRAT = '{0[0]} {0[1]} STRAT'
FUNC_END = '{0[0]} {0[1]} END'
FUNC_LOCATION = '{0[0]} {0[1]} LINE:{0[2]}'

LOG_INFO = "I"
LOG_WARNING = "W"
LOG_ERROR = "E"
LOG_CRITICAL = "C"
LOG_DUBUG = "D"


def output(msg_format: str, *msg_array):
    msg_id = msg_array[0][0]
    if msg_id == LOG_INFO:
        logging.info(msg_format.format(msg_array))
    elif msg_id == LOG_WARNING:
        logging.warning(msg_format.format(msg_array))
    elif msg_id == LOG_ERROR:
        logging.error(msg_format.format(msg_array))
    elif msg_id == LOG_CRITICAL:
        logging.critical(msg_format.format(msg_array))
    elif msg_id == LOG_DUBUG:
        logging.debug(msg_format.format(msg_array))
    else:
        logging.info(msg_format.format(msg_array))


def location():
    frame = inspect.currentframe().f_back
    path = '{}'.format(frame.f_code.co_name)
    sub_path = pathlib.Path(path)
    return FUNC_LOCATION.format([sub_path, frame.f_code.co_name, frame.f_lineno])


def main():
    frame = inspect.currentframe().f_back
    print(frame.f_code.co_names)
    print(frame.f_code.co_argcount)
    print(location())


if __name__ == '__main__':
    main()
    output(FUNC_STRAT, "IDDDDD", location())
