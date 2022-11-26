from pathlib import Path

BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
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
LOG_DATETIME_FORMAT = '%d.%m.%Y %H:%M:%S'
LOGS_DIR = 'logs'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
MAIN_DOC_URL = 'https://docs.python.org/3/'
MAIN_PEP_URL = 'https://peps.python.org/'
RESULTS_DIR = 'results'
