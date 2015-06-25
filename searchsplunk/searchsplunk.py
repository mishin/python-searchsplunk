import requests
import re
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


class SearchSplunk(Splunk):
    """
    Splunk search class
    """
    def search(self, search_query):
        """
        Create searches in Splunk and get the response.
        Returns True or raises exception
        Search result accessible through SearchSplunk.search_results
        """
        self.search_query = search_query

        self._start_search()

        search_done = False
        while not search_done:
            if self._search_status():
                search_done = True
                self._search_results()
        return True

    def _start_search(self):
        uri = '/services/search/jobs' 
        method = 'POST'

        if not self.search_query.startswith('search'):
            self.search_query = '{0} {1}'.format('search ', self.search_query)

        s = self.request(method, uri, body={'search': self.search_query})
        self.sid = minidom.parseString(s.text).getElementsByTagName('sid')[0].childNodes[0].nodeValue
        return True

    def _search_status(self):
        uri = '/services/search/jobs/{0}/'.format(self.sid)
        method = 'GET'

        s = self.request(method, uri)
        return int(re.compile('isDone">(0|1)').search(s.text).groups()[0])

    def _search_results(self, output_mode='json'):
        uri = '/services/search/jobs/{0}/results/'.format(self.sid)
        method = 'GET'

        s = self.request(method, uri, params={'output_mode': output_mode})
        self.s = s
        self.search_results = s.json()
        return True
