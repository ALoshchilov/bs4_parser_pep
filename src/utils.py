import logging

from requests import RequestException

from exceptions import ParserFindTagException
from messages import DOWNLOAD_URL_ERROR, TAG_NOT_FOUND


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            DOWNLOAD_URL_ERROR.format(url=url),
            stack_info=True
        )


def find_tag(soup, tag=None, attrs=None, text=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}), text=text)
    if searched_tag is None:
        error_message = TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        logging.error(error_message, stack_info=True)
        raise ParserFindTagException(error_message)
    return searched_tag
