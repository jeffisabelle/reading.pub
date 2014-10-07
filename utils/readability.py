import requests
import settings

TOKEN = settings.READABILITY_TOKEN
BASE_URL = "https://readability.com"
PARSE_ENDPOINT = "/api/content/v1/parser"


def make_readable(url):
    """

    Arguments:
    - `url`:
    """
    payload = {'token': TOKEN, 'url': url}
    request_url = BASE_URL + PARSE_ENDPOINT
    json_data = requests.get(request_url, params=payload)
    return json_data.json()


if __name__ == '__main__':
    print make_readable(
        "http://robertheaton.com/2014/03/07/lessons-from-a-silicon-valley-job-search/"
    )["word_count"]
