import sys
from struct import pack

# https://code.google.com/p/leveldb-py/
import leveldb

from inserter_maker import open_db


def main():
	db_path = sys.argv[1]
	db = open_db(db_path)
	for k, v in db.iterator().seekFirst():
		print repr(k), repr(v)
	db.close()


if __name__ == '__main__':
	main()
