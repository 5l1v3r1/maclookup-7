# Mac Lookup tool

This is a simple CLI tool for doing a MAC lookup against the database at macaddress.io.

Given a MAC address, it will return the associated Vendor name.

It is written for Python3, and can be run as a standalone Python app, or via Docker.

## Requirements

* Either Python3, or Docker installed
* An API key from https://macaddress.io/signup. This must be set as the environment variable `$MAC_API_KEY`

## Usage

Clone this repo, then run either with or without Docker

### Running on host, without Docker:

```bash
vagrant@ubuntu-bionic:~/maclookup$ export MAC_API_KEY=S3cr3tK3y
vagrant@ubuntu-bionic:~/maclookup$ ./maclookup.py a4:5e:60:c7:e6:ff
Apple, Inc
vagrant@ubuntu-bionic:~/maclookup$ ./maclookup.py invalidmac
HTTP Error code: 422
Invalid MAC or OUI address was received.
vagrant@ubuntu-bionic:~/maclookup$
```

### Running via Docker:

```bash
vagrant@ubuntu-bionic:~/maclookup$ docker-compose run --rm maclookup a4:5e:60:c7:e6:ff
Building maclookup
Step 1/3 : FROM python:3-alpine
3-alpine: Pulling from library/python
921b31ab772b: Pull complete
1a0c422ed526: Pull complete
3f995998f0d2: Pull complete
1e10683833cd: Pull complete
57b74f627661: Pull complete
Digest: sha256:fabd15bc1b5c6f4097cabae02122250f51d6fda4ab4729d1ba17f01028a7fc15
Status: Downloaded newer image for python:3-alpine
 ---> 828bce60a61c
Step 2/3 : ADD maclookup.py /
 ---> 600a79dd164c
Step 3/3 : ENTRYPOINT [ "python",  "./maclookup.py" ]
 ---> Running in 4f8a40deeb70
Removing intermediate container 4f8a40deeb70
 ---> 6d82de72025f
Successfully built 6d82de72025f
Successfully tagged maclookup_maclookup:latest
WARNING: Image for service maclookup was built because it did not already exist. To rebuild this image you must use `docker-compose build` or `docker-compose up --build`.
You must obtain an API Key from https://macaddress.io/signup
Set it as the environment variable MAC_API_KEY
vagrant@ubuntu-bionic:~/maclookup$ export MAC_API_KEY=S3cr3tK3y
vagrant@ubuntu-bionic:~/maclookup$ docker-compose run --rm maclookup a4:5e:60:c7:e6:ff
Apple, Inc
vagrant@ubuntu-bionic:~/maclookup$
```

## Return Codes

* Successful query - exit code `0`
* Not providing exactly one CLI argument - `255`
* Failure to set `$MAC_API_KEY` env var - `2`
* HTTP or URL error, e.g. unable to connect, or API error: `1`. It will also publish the failure reason.


## Todo/Improvements

* Using the [maclookup](https://pypi.org/project/maclookup/) library would be much simpler. It was written this way
  as an exercise.
* Using `requests()` would also be simpler and better, and do better SSL certification validation. This would be better
  for security
* It should do better validation of the result, e.g. identifying when there is no vendor. Currently that is returned
  as a blank string.
* It would be good to offer full data, as an option, e.g. with `-j` to return a JSON dump. 
* Basic MAC address format validation could be done on the client side, prior to making the API call.
* Add some basic tests & linting checks via CircleCI
