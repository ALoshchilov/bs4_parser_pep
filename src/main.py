import logging
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, MAIN_PEP_URL
from messages import (
    ARGS_INFO, DOWNLOAD_SUCCESS, EMPTY_RESPONSE_ERROR, NOTHING_FOUND,
    PARSER_FINISHED, PARSER_STARTED, STATUS_NOT_MATCH, UNKNOWN_STATUS
)
from outputs import control_output
from utils import get_response, find_tag


def get_soup(session, url, features='lxml'):
    response = get_response(session, url)
    if response is None:
        raise ValueError(EMPTY_RESPONSE_ERROR.format(url=url))
    return BeautifulSoup(response.text, features)


def whats_new(
    session,
    rel_url='whatsnew/',
    output_headers=('Ссылка на статью', 'Заголовок', 'Редактор, Автор')
):
    whats_new_url = urljoin(MAIN_DOC_URL, rel_url)
    main_div = find_tag(
       get_soup(session, whats_new_url),
       'section',
       attrs={'id': 'what-s-new-in-python'}
    )
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [output_headers]
    for section in tqdm(sections_by_python):
        version_a_tag = section.find('a')
        href = version_a_tag['href']
        version_link = urljoin(whats_new_url, href)
        soup = get_soup(session, version_link)
        results.append(
            (
                version_link,
                find_tag(soup, 'h1').text,
                find_tag(soup, 'dl').text.replace('\n', ' ')
            )
        )
    return results


def latest_versions(
    session,
    output_headers=('Ссылка на документацию', 'Версия', 'Статус')
):
    sidebar = find_tag(
        get_soup(session, MAIN_DOC_URL),
        'div',
        attrs={'class': 'sphinxsidebarwrapper'}
    )
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All version' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ValueError(NOTHING_FOUND)
    results = [output_headers]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''

        results.append((a_tag['href'], version, status))
    return results


def download(
    session,
    rel_url='download.html',
    rel_path='downloads'
):
    downloads_url = urljoin(MAIN_DOC_URL, rel_url)
    downloads_dir = BASE_DIR / rel_path
    main_tag = find_tag(
        get_soup(session, downloads_url), 'div', attrs={'role': 'main'}
    )
    table_tag = find_tag(main_tag, 'table', attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    archive_url = urljoin(downloads_url, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
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
    pep_url=MAIN_PEP_URL,
    output_headers=('Статус', 'Количество')
):
    numerical_idx_tag = find_tag(
        get_soup(session, pep_url), 'section', attrs={'id': 'numerical-index'}
    )
    tbody_tag = find_tag(numerical_idx_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')

    results = {}
    messages = []
    for tr in tqdm(tr_tags):
        status_key = find_tag(tr, 'td').text[1:]
        expected_status = EXPECTED_STATUS.get(status_key)
        if not expected_status:
            logging.info(UNKNOWN_STATUS.format(status_key=status_key))
        pep_link = urljoin(pep_url, find_tag(tr, 'a')['href'])
        actual_status = find_tag(
            get_soup(session, pep_link), text='Status'
        ).find_next('dd').text
        if actual_status not in expected_status:
            messages.append(
                STATUS_NOT_MATCH.format(
                    pep_link=pep_link,
                    actual_status=actual_status,
                    expected_status=expected_status
                )
            )
        results[actual_status] = results.get(actual_status, 0) + 1
    for message in messages:
        logging.info(message)
    results = list(results.items())
    # results.append(('Total', len(results)))
    return (
        output_headers,
        results,
        ('Total', len(results))
    )


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
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


if __name__ == '__main__':
    main()
