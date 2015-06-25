import requests
import re
from xml.dom import minidom
import warnings

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
        print r.status_code, r.text
        try:
            self.session_key = minidom.parseString(r.text).getElementsByTagName('sessionKey')[0].childNodes[0].nodeValue
        except IndexError:
            raise SplunkInvalidCredentials(r.text)
        return

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
        Returns a Python object
        """
        self.search_query = search_query

        self._start_search()

        search_done = False
        while not search_done:
            if self._search_status():
                search_done = True
                self._search_results()
        return self.search_results

    def _start_search(self):
        uri = '/services/search/jobs' 
        method = 'POST'

        if not self.search_query.startswith('search'):
            self.search_query = '{0} {1}'.format('search ', self.search_query)

        s = self.request(method, uri, body={'search': self.search_query})
        print s.text
        self.sid = minidom.parseString(s.text).getElementsByTagName('sid')[0].childNodes[0].nodeValue
        return

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
        return


class SplunkError(Exception):
    pass


class SplunkInvalidCredentials(SplunkError):
    pass
