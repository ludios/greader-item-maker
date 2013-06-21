#!/usr/bin/env python

import sys
from struct import pack

import urllib
from inserter_maker import open_db, unreversed_encoded_url


def main():
	db_path = sys.argv[1]
	start = sys.argv[2]
	db = open_db(db_path)
	for k, v in db.iterator().seek(start):
		if k.startswith('$'):
			continue
		if not k.startswith(start):
			break
		print urllib.unquote_plus(unreversed_encoded_url(k))
	db.close()


if __name__ == '__main__':
	main()
