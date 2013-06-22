#!/usr/bin/python

import sys
import urllib

try:
	import simplejson as json
except ImportError:
	import json

"""
Parses concatenated reqres logs and outputs status 200 URLs that should be inserted into
greader-stats database.
"""

def get_feed_url(greader_url):
	assert greader_url.startswith('https://www.google.com/reader/api/0/stream/contents/feed/'), greader_url
	assert greader_url.endswith('r=n&n=1000&hl=en&likes=true&comments=true&client=ArchiveTeam'), greader_url
	encoded_feed_url = greader_url.replace('https://www.google.com/reader/api/0/stream/contents/feed/', '', 1).rsplit('?', 1)[0]
	return urllib.unquote_plus(encoded_feed_url)


def main():
	for line in sys.stdin:
		data = json.loads(line)
		assert isinstance(data['status_code'], basestring)
		if data['status_code'] == '200':
			greader_url = data['url']
			print get_feed_url(greader_url)
			# Dupes will be printed for continued URLs, but that's okay
			

if __name__ == '__main__':
	main()
