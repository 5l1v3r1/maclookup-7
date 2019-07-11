FROM python:3-alpine

ADD maclookup.py /

ENTRYPOINT [ "python",  "./maclookup.py" ]
