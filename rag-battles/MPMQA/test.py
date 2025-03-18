#!/usr/bin/env python3
import requests
from pm209 import files

def test_link(link):
    try:
        response = requests.head(link, allow_redirects=True, timeout=5)
        if response.status_code >= 400:
            response = requests.get(link, allow_redirects=True, timeout=5)
        return response.status_code, response.url
    except requests.RequestException as e:
        return None, str(e)

def main():
    for link in files:
        status_code, info = test_link(link)
        if status_code is None:
            print(f"Link: {link}\n  Error: {info}\n")
        elif status_code != 200:
            print(f"Link: {link}\n  Status Code: {status_code}\n  Final URL: {info}\n")

if __name__ == '__main__':
    main()
