import logging
import re
from urllib.parse import urljoin

import requests_cache
from collections import defaultdict
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOAD_REL_PATH, DOWNLOAD_REL_URL,
                       EXPECTED_STATUS, LOGGER, MAIN_DOC_URL, MAIN_PEP_URL)
from messages import (ARGS_INFO, DOWNLOAD_SUCCESS, EMPTY_RESPONSE_ERROR,
                      LAST_FRONTIER_ERROR, NOTHING_FOUND, PARSER_FINISHED,
                      PARSER_STARTED, STATUS_NOT_MATCH, UNKNOWN_STATUS)
from outputs import control_output
from utils import find_tag, get_response, get_soup


def whats_new(
    session,
    rel_url='whatsnew/',
):
    whats_new_url = urljoin(MAIN_DOC_URL, rel_url)
    results = []
    messages = []
    for section in tqdm(get_soup(session, whats_new_url).select(
        '#what-s-new-in-python div.toctree-wrapper:first-of-type li.toctree-l1'
    )):
        try:
            version_a_tag = section.find('a')
            href = version_a_tag['href']
            version_link = urljoin(whats_new_url, href)
            soup = get_soup(session, version_link)
        except AttributeError:
            messages.append(
                ('error', EMPTY_RESPONSE_ERROR.format(url=version_link))
            )
            continue
        results.append(
            (
                version_link,
                find_tag(soup, 'h1').text,
                find_tag(soup, 'dl').text.replace('\n', ' ')
            )
        )
    for (message_type, text) in messages:
        LOGGER[message_type](text)
    return [
        ('Ссылка на статью', 'Заголовок', 'Редактор, Автор'),
        *results,
    ]


def latest_versions(
    session
):
    sidebar = find_tag(
        get_soup(session, MAIN_DOC_URL),
        'div',
        attrs={'class': 'sphinxsidebarwrapper'}
    )
    for ul in sidebar.find_all('ul'):
        if 'All version' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ValueError(NOTHING_FOUND)
    results = []
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''

        results.append((a_tag['href'], version, status))
    return [
        ('Ссылка на документацию', 'Версия', 'Статус'),
        *results,
    ]


def download(
    session,
    rel_url=DOWNLOAD_REL_URL,
    rel_path=DOWNLOAD_REL_PATH
):
    downloads_url = urljoin(MAIN_DOC_URL, rel_url)
    pdf_a4_tag = get_soup(session, downloads_url).select_one(
        'table.docutils a[href$="-pdf-a4.zip"]'
    )
    archive_url = urljoin(downloads_url, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / rel_path
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = get_response(session, downloads_url)
    if response is None:
        return
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(DOWNLOAD_SUCCESS.format(path=downloads_dir))


def pep(
    session,
    pep_url=MAIN_PEP_URL
):
    numerical_idx_tag = find_tag(
        get_soup(session, pep_url), 'section', attrs={'id': 'numerical-index'}
    )
    tbody_tag = find_tag(numerical_idx_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    results = defaultdict(int)
    messages = []
    for tr in tqdm(tr_tags):
        try:
            status_key = find_tag(tr, 'td').text[1:]
            expected_status = EXPECTED_STATUS.get(status_key)
            if not expected_status:
                messages.append(
                    ('info', UNKNOWN_STATUS.format(status_key=status_key))
                )
            pep_link = urljoin(pep_url, find_tag(tr, 'a')['href'])
            actual_status = find_tag(
                get_soup(session, pep_link), text='Status'
            ).find_next('dd').text
        except AttributeError:
            messages.append(
                ('error', EMPTY_RESPONSE_ERROR.format(url=pep_link))
            )
            continue
        if actual_status not in expected_status:
            messages.append((
                'info',
                STATUS_NOT_MATCH.format(
                    pep_link=pep_link,
                    actual_status=actual_status,
                    expected_status=expected_status
                )
            ))
        results[actual_status] += 1
    for (message_type, text) in messages:
        LOGGER[message_type](text)
    return (
        ('Статус', 'Количество'),
        *results.items(),
        ('Total', sum(results.values()))
    )


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    try:
        configure_logging()
        logging.info(PARSER_STARTED)
        arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
        args = arg_parser.parse_args()
        logging.info(ARGS_INFO.format(args=args))
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
        logging.info(PARSER_FINISHED)
    except Exception as error:
        logging.exception(LAST_FRONTIER_ERROR.format(
            error=error
        ))


if __name__ == '__main__':
    main()
