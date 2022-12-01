from pathlib import Path

# Константы для работы с файловой системой
BASE_DIR = Path(__file__).parent
LOGS_DIR = 'logs'
LOG_FILENAME = 'parser.log'
RESULTS_DIR = 'results'
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
log_dir = BASE_DIR / LOGS_DIR
log_file = log_dir / LOG_FILENAME
results_dir = BASE_DIR / RESULTS_DIR

# Константы для работы с сетевыми запросами
MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'

# Константы для настройки логирования
LOG_DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

# Константы для работы парсера
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
