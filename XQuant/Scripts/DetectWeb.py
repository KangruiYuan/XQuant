import requests
from requests.exceptions import ConnectionError


def getHttpStatusCode(url):
    try:
        request = requests.get(url)
        httpStatusCode = request.status_code
        return httpStatusCode
    except ConnectionError as e:
        print(e)
        return None


if __name__ == "__main__":
    URLS = {"XQuant": "http://localhost:9999"}

    for name in URLS.keys():
        status = getHttpStatusCode(URLS[name])
        if status is not None:
            print(f"{name}:{URLS[name]}[CODE={status}]")
        if status is None or status != 200:
            pass
