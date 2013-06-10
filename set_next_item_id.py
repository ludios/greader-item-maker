import sys
from struct import pack

# https://code.google.com/p/leveldb-py/
import leveldb

from inserter_maker import open_db


def main():
	db_path = sys.argv[1]
	next_item_id = int(sys.argv[2])
	db = open_db(db_path)
	db.put("$next_item_id$", pack("<i", next_item_id))


if __name__ == '__main__':
	main()
