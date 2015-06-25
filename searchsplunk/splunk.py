import requests
import warnings
from xml.dom import minidom
from . import exceptions


warnings.filterwarnings('ignore')

class Splunk(object):
    """
    Splunk base class
    """
    def __init__(self, base_url, username, password, ssl_verify=True):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.ssl_verify = ssl_verify
        self.session_key = None
        return

    def login(self):
        """
        Sets a session key
        """
        uri='/services/auth/login'
        method='POST'

        r = self.request(method, uri, body={'username': self.username, 'password': self.password})
        try:
            self.session_key = minidom.parseString(r.text).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
        except IndexError:
            raise exceptions.SplunkInvalidCredentials(r.text)
        return True

    @property
    def headers(self):
        """
        Create basic headers
        """
        if self.session_key:
            headers = {'Authorization': 'Splunk {0}'.format(self.session_key)}
        else:
             headers = {}
        return headers

    def request(self, method, uri, body={}, params={}, headers={}, auth=()):
        """
        uri: /some/cool/uri
        method: post, get, put, delete      
        body: body data
        params: get parameters
        headers: http headers
        auth: auth tuple username, password

        Returns an HTTP response object
        """
        headers.update(self.headers)
        return requests.request(method, '{0}{1}'.format(self.base_url, uri),
                                headers=headers, data=body, params=params, 
                                auth=auth, verify=self.ssl_verify)
