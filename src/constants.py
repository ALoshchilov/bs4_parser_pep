import logging
from pathlib import Path

# Константы для работы с файловой системой
BASE_DIR = Path(__file__).parent
DOWNLOAD_REL_PATH = 'downloads'
LOGS_DIR = 'logs'
LOG_FILENAME = 'parser.log'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_DIR = BASE_DIR / LOGS_DIR
LOG_FILE = LOG_DIR / LOG_FILENAME
RESULT_DIR = 'results'

# Константы для работы с сетевыми запросами
DOWNLOAD_REL_URL = 'download.html'
MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'

# Константы для настройки логирования
LOG_DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
LOGGER = {
    'error': logging.error,
    'info': logging.info
}


# Константы для настройки парсера
EXPECTED_STATUS = {
    'A': ['Active', 'Accepted'],
    'D': ['Deferred'],
    'F': ['Final'],
    'P': ['Provisional'],
    'R': ['Rejected'],
    'S': ['Superseded'],
    'W': ['Withdrawn'],
    '': ['Draft', 'Active']
}
FILE = 'file'
PRETTY = 'pretty'
