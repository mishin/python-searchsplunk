# python-searchsplunk
Easily create Splunk searches from Python and get the result as a Python object.

# requires
- requests: https://pypi.python.org/pypi/requests

# usage instructions

```python
>>> from searchsplunk import SearchSplunk
>>> import pprint
>>> pp = pprint.PrettyPrinter(indent=2)
>>> s = SearchSplunk('https://splunk.acme.com:8089', 'MYUSER', 'MYPASS', ssl_verify=False)
>>> s.login()
>>> s.search('sourcetype=salt:grains openstack_uid=e0303456c-d5a3-789f-ab68-8f27561ffa0f | dedup openstack_uid')
>>> pp.pprint(d)
{ u'fields': [ { u'name': u'_bkt'},
               { u'name': u'_cd'},
               { u'name': u'_indextime'},
               { u'name': u'_kv'},
               { u'name': u'_raw'},
               { u'name': u'_serial'},
               { u'name': u'_si'},
               { u'name': u'_sourcetype'},
               { u'name': u'_subsecond'},
               { u'name': u'_time'},
               { u'name': u'host'},
               { u'name': u'index'},
               { u'name': u'linecount'},
               { u'name': u'openstack_uid'},
               { u'name': u'source'},
               { u'name': u'sourcetype'},
               { u'name': u'splunk_server'}],
  u'init_offset': 0,
  u'messages': [],
  u'preview': False,
  u'results': [ { u'_bkt': u'main~1122~25B521A6-9612-407D-A1BA-F8KJSEBB7628',
                  u'_cd': u'1122:290410720',
                  u'_indextime': u'1435071966',
                  u'_kv': u'1',
                  u'_raw': "backedup: 'True'\nddns_hostname: server-7654.acme.com\nopenstack_uid: e0303456c-d5a3-789f-ab68-8f27561ffa0f\n",
                  u'_serial': u'0',
                  u'_si': [u'splunkserv', u'main'],
                  u'_sourcetype': u'salt:grains',
                  u'_time': u'2015-06-23T11:06:05.000-04:00',
                  u'host': u'server-7654.acme.com',
                  u'index': u'main',
                  u'linecount': u'17',
                  u'openstack_uid': u'e0303456c-d5a3-789f-ab68-8f27561ffa0f',
                  u'source': u'/etc/salt/grains',
                  u'sourcetype': u'salt:grains',
                  u'splunk_server': u'splunkmaster'}]}
```
