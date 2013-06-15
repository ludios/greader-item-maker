#!/usr/bin/env python

import sys
from struct import pack

from inserter_maker import open_db


def main():
	db_path = sys.argv[1]
	start = sys.argv[2]
	db = open_db(db_path)
	for k, v in db.iterator().seek(start):
		print repr(k), repr(v)
	db.close()


if __name__ == '__main__':
	main()
