from requests import RequestException

from exceptions import ParserFindTagException
from messages import DOWNLOAD_URL_ERROR, TAG_NOT_FOUND


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        raise RequestException(DOWNLOAD_URL_ERROR.format(url=url))


def find_tag(soup, tag=None, attrs=None, text=None):
    searched_tag = soup.find(
        tag,
        attrs={} if attrs is None else attrs,
        text=text
    )
    if searched_tag is None:
        raise ParserFindTagException(
            TAG_NOT_FOUND.format(tag=tag, attrs=attrs)
        )
    return searched_tag
