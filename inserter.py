#!/usr/bin/python

import os
import psycopg2
import sys
import urllib

def main():
	try:
		password = os.environ['GREADER_DB_PASS']
	except KeyError:
		password = ''
	conn = psycopg2.connect("dbname='greader' user='greader' host='192.168.1.20' password='%s'" % (password,))
	cur = conn.cursor()
	cur.execute("select * from counters")
	rows = cur.fetchall()
	print rows

if __name__ == '__main__':
	main()
