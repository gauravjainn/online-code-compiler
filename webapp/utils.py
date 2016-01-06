import json
import uuid

import requests

from django.http import HttpResponse, HttpResponseBadRequest


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def HttpJSONResponse(data, status=200):
    return HttpResponse(json.dumps(data), status=status, content_type="application/json")


def exception_response(e):
    error = {
        'error': True,
        'message': "%s - %s" % (e.__doc__, repr(e))
    }

    return HttpJSONResponse(data, status=500)


def exception_handler(func):
    def wrap_exception(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return exception_response(e)

    return wrap_exception


def generate_unique_uri():
    # Some other approach?
    return uuid.uuid4().hex


def code_compile_result(lang, source):

    RUN_URL = 'https://api.hackerearth.com/v3/code/run/'
    CLIENT_SECRET = '2a277f2591e3a56e07f8d1249a51dee17320818a'

    data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'lang': lang,
        'time_limit': 5,
        'memory_limit': 262144,
    }

    try:
        r = requests.post(RUN_URL, data=data, timeout=10)
        return r.json()
    except:
        return None
