#!/usr/bin/env python3

# This utility takes a single MAC address parameter, and queries the macaddress.io API
# for the company name associated with that MAC.

# You will need an API Key for macaddress.io. Signup at https://macaddress.io/signup
# This needs to passed in as an environment parameter - MAC_API_KEY=<key>

# Example usage:
# ./maclookup.py a4:5e:60:c7:e6:ff
# Example result:
# 'Apple, Inc'

# Successful queries will exit with code 0
# Errors such as missing API key, incorrect number of arguments, HTTP error, etc will
# return a non-zero code

# Lindsay Hill (lindsay.k.hill@gmail.com)

import os
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

API_URL = 'https://api.macaddress.io/v1'


def main():

    # We expect exactly one argument, a MAC address
    # Should probably do MAC validation here, but it is done by API
    if len(sys.argv) != 2:
        print('You must provide a single MAC address as input parameter')
        print('For example, ./maclookup.py a4:5e:60:c7:e6:ff')
        sys.exit(255)

    mac_address = sys.argv[1]

    # Setting API Key as an environment variable to avoid storing it on disk
    try:
        api_key = os.environ['MAC_API_KEY']
    except KeyError:
        print('You must obtain an API Key from https://macaddress.io/signup')
        print('Set it as the environment variable MAC_API_KEY')
        sys.exit(2)

    url = API_URL + '?output=vendor&search=' + mac_address

    req = Request(url)
    req.add_header('X-Authentication-Token', api_key)
    try:
        response = urlopen(req)
    except HTTPError as e:
        print('HTTP Error code:', e.code)
        print(e.read().decode('utf-8'))
        sys.exit(1)
    except URLError as e:
        print('Failed to connect to api.macaddress.io')
        print('Reason:', e.reason)
        sys.exit(1)

    # Could do better checking in here, for example if no vendor found, it returns blank here.
    print(response.read().decode('utf-8'))


if __name__ == "__main__":
    main()
