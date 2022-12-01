import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import (
    BASE_DIR, DATETIME_FORMAT, FILE, PRETTY, RESULTS_DIR  # , results_dir
)
from messages import RESULTS_SAVED


def default_output(results):
    for row in results:
        print(*row)


def pretty_output(results, cli_args):
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / RESULTS_DIR
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        csv.writer.unix_dialect(f)
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(RESULTS_SAVED.format(file_path=file_path))


MODES = {
    PRETTY: pretty_output,
    FILE: file_output,
}


def control_output(results, cli_args):
    output = MODES.get(cli_args.output)
    if output is None:
        default_output(results)
    else:
        output(results, *(cli_args,))
