#!/usr/bin/python

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE
import sys
import urllib

py_ver = sys.version[0:3].replace(".", "")
quiet = True

def main():
	try:
		password = os.environ['GREADER_DB_PASS']
	except KeyError:
		password = ''
	conn = psycopg2.connect("dbname='greader' user='greader' host='192.168.1.20' password='%s'" % (password,))
	conn.set_isolation_level(ISOLATION_LEVEL_SERIALIZABLE)
	cur = conn.cursor()
	if quiet:
		print "'Quiet mode enabled; will print every 10000 input lines"
	for n, feed_url in enumerate(sys.stdin):
		if n % 10000 == 0:
			print n
		feed_url = feed_url.rstrip()
		if not feed_url:
			continue
		encoded_url = urllib.quote_plus(feed_url)
		url_encoding_method = "py%s_quote_plus" % (py_ver,)
		dont_download = False
		job_ids = []
		try:
			cur.execute(
				"INSERT INTO feeds (encoded_url, feed_url, url_encoding_method, dont_download, job_ids) VALUES (%s, %s, %s, %s, %s)",
				(encoded_url, feed_url, url_encoding_method, dont_download, job_ids))
			conn.commit()
		except psycopg2.IntegrityError, e:
			if 'duplicate key value violates unique constraint' in str(e):
				if not quiet:
					print "%r already in table" % (encoded_url,)
				conn.rollback()
			else:
				raise
		else:
			if not quiet:
				print "Inserted %r" % (encoded_url,)

if __name__ == '__main__':
	main()
