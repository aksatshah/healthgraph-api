"""Python Client Library for Health Graph API (http://developer.runkeeper.com/healthgraph). 

The API is used for accessing RunKeeper (http://runkeeper.com) for retrieving, 
updating, deleting and uploading Fitness Activity and Health Measurements Information.

This module implements sessions for making REST requests to the Health Graph API.

"""

import requests
import exceptions
import settings
from time import mktime
from datetime import datetime
from wsgiref.handlers import format_date_time
import pdb


__author__ = "Ali Onur Uyar"
__copyright__ = "Copyright 2012, Ali Onur Uyar"
__credits__ = []
__license__ = "GPL"
__version__ = "0.3.0"
__email__ = "aouyar at gmail.com"
__status__ = "Development"
    
    
class Session(object):
    
    def __init__(self, access_token):
        self._access_token = access_token
        
    def request(self, request_type, resource, content_type=None, 
                params=None, data=None, modified_since=None):
        headers = {'Authorization': "Bearer %s" % self._access_token,}
        headers['If-Modified-Since'] = modified_since
        content_header = None
        if content_type is not None:
            if request_type == 'GET':
                content_header = 'Accept'
            elif request_type in ('POST', 'PUT'):
                content_header = 'Content-Type'
            else:
                content_header = None
            if content_header is not None:
                headers[content_header] = ('application/vnd.com.runkeeper.%s+json'
                                           % content_type)
        url = settings.API_URL + resource
        req = requests.request(request_type, url, headers=headers, 
                               params=params, data=data)
        return req
    
    def get(self, resource, content_type=None, params=None, modified_since=None):
        return self.request('GET', resource, content_type, params=params, modified_since=modified_since)
    
    def post(self, resource, content_type=None, data=None):
        return self.request('POST', resource, content_type, data=data)
        
    def put(self, resource, content_type=None, data=None):
        return self.request('PUT', resource, content_type, data=data)
    
    def delete(self, resource):
        return self.request('DELETE', resource)
        
    def head(self, resource, content_type=None, params=None):
        return self.request('HEAD', resource, content_type, params=params)


class NullSession(Session):

    def __init__(self):
        self._access_token = None
        
    def request(self, request_type, resource, content_type=None, 
            params=None, data=None):
        raise exceptions.NoSessionError()


_default_session = NullSession()

def init_session(access_token):
    global _default_session
    _default_session = Session(access_token)
    
def get_session():
    return _default_session
    