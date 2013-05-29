#!/usr/bin/python

import os
import psycopg2
import subprocess
from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE
import sys
import urllib

num_urls_in_item = 200

class Stop(Exception):
	pass

def try_makedirs(p):
	try:
		os.makedirs(p)
	except OSError:
		pass

def make_an_item(conn, cur):
	cur.execute("SELECT count FROM counters WHERE name = %s", ("next_item_id",))
	next_item_id = cur.fetchall()[0][0]
	item_name = str(next_item_id).zfill(10)
	print "Maybe generating item %s..." % (item_name,),
	cur.execute("SELECT encoded_url FROM feeds WHERE dont_download = false AND job_ids = %s LIMIT " + str(num_urls_in_item), ([],))
	encoded_urls = list(row[0] for row in cur.fetchall())
	if len(encoded_urls) < num_urls_in_item:
		print "NO"
		print "Only have %d URLs not assigned to a job, need %d; stopping" % (len(encoded_urls), num_urls_in_item)
		raise Stop()
	cur.execute("UPDATE feeds SET job_ids = array_append(job_ids, %s) WHERE encoded_url IN %s", (next_item_id, tuple(encoded_urls)))
	cur.execute("UPDATE counters SET count = %s WHERE name = %s", (next_item_id + 1, "next_item_id"))
	conn.commit()
	print "OK"
	return item_name, encoded_urls

def write_item(items_root, item_name, encoded_urls):
	assert encoded_urls, encoded_urls
	assert len(item_name) == 10, item_name
	fdir = os.path.join(items_root, item_name[0:6])
	try_makedirs(fdir)
	fname = os.path.join(fdir, item_name)
	assert not os.path.exists(fname), fname
	assert not os.path.exists(fname + ".gz"), fname
	with open(fname + ".tmp", "wb") as f:
		f.write("\n".join(encoded_urls) + "\n")
	subprocess.call(["gzip", "-9", fname + ".tmp"])
	os.rename(fname + ".tmp.gz", fname + ".gz")

def main():
	items_root = sys.argv[1]
	try:
		password = os.environ['GREADER_DB_PASS']
	except KeyError:
		password = ''
	conn = psycopg2.connect("dbname='greader' user='greader' host='192.168.1.20' password='%s'" % (password,))
	conn.set_isolation_level(ISOLATION_LEVEL_SERIALIZABLE)
	cur = conn.cursor()
	while True:
		try:
			item_name, encoded_urls = make_an_item(conn, cur)
		except Stop:
			break
		else:
			write_item(items_root, item_name, encoded_urls)

if __name__ == '__main__':
	main()
