#!/usr/bin/python

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE
import sys
import urllib

num_urls_in_item = 200

class Stop(Exception):
	pass

def make_an_item(conn, cur):
	cur.execute("SELECT count FROM counters WHERE name = %s", ("next_item_id",))
	next_item_id = cur.fetchall()[0][0]
	item_name = str(next_item_id).zfill(10)
	print "Generating item %s" % (item_name,)
	cur.execute("SELECT encoded_url FROM feeds WHERE job_ids = %s LIMIT " + str(num_urls_in_item), ([],))
	encoded_urls = list(row[0] for row in cur.fetchall())
	if len(encoded_urls) < num_urls_in_item:
		print "Only have %d URLs not assigned to a job, need %d; stopping" % (len(encoded_urls), num_urls_in_item)
		raise Stop()
	# Don't use encoded_urls until we commit
	cur.execute("UPDATE feeds SET job_ids = array_append(job_ids, %s) WHERE encoded_url IN %s", (next_item_id, tuple(encoded_urls)))
	cur.execute("UPDATE counters SET count = %s WHERE name = %s", (next_item_id + 1, "next_item_id"))
	conn.commit()
	print "\n".join(encoded_urls)

def main():
	try:
		password = os.environ['GREADER_DB_PASS']
	except KeyError:
		password = ''
	conn = psycopg2.connect("dbname='greader' user='greader' host='192.168.1.20' password='%s'" % (password,))
	conn.set_isolation_level(ISOLATION_LEVEL_SERIALIZABLE)
	cur = conn.cursor()
	while True:
		try:
			make_an_item(conn, cur)
		except Stop:
			break

if __name__ == '__main__':
	main()
