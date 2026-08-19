import os


def get_timeout_seconds():
    return 30


def fetch_status(url):
    timeout = 30
    return {"url": url, "timeout": timeout}
