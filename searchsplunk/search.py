import re
from xml.dom import minidom
from .splunk import Splunk

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
