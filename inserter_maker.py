#!/usr/bin/env python

import os
import sys
import urllib
import gzip
import time
from struct import pack, unpack

# https://code.google.com/p/leveldb-py/
import leveldb

_postImportVars = vars().keys()


# Just for progress output
lines_per_print = 10000

parent = os.path.dirname

def try_makedirs(p):
	try:
		os.makedirs(p)
	except OSError:
		pass


def get_item_fname(items_root, item_id):
	item_name = str(item_id).zfill(10)
	assert len(item_name) == 10, item_name
	fdir = os.path.join(items_root, item_name[0:6])
	fname = os.path.join(fdir, item_name) + ".gz"
	return fname


def write_item(items_root, item_id, encoded_urls):
	assert encoded_urls, encoded_urls

	fname = get_item_fname(items_root, item_id)
	assert not os.path.exists(fname + ".tmp"), fname
	try_makedirs(parent(fname))
	f = gzip.open(fname + ".tmp", "wb")
	try:
		f.write("\n".join(sorted(encoded_urls)) + "\n")
	finally:
		f.close()
	assert not os.path.exists(fname), fname
	os.rename(fname + ".tmp", fname)


def encode_item_ids(ids):
	return "".join(pack("<I", n) for n in ids)


def decode_item_ids(ids):
	return unpack("<I", ids)


def reversed_encoded_url(url):
	if not (url.startswith("http%3A%2F%2F") or url.startswith("https%3A%2F%2F")):
		raise ValueError("Encoded URL must have http or https schema: %r" % (url,))
	schema, rest = url.split("%3A%2F%2F", 1)
	# domain is separated from port_path_query by %3A (:) or %2F (/)
	try:
		domain, port_path_query = rest.split("%", 1)
	except ValueError:
		domain = rest
		port_path_query = None
	reversed_domain = '.'.join(domain.split('.')[::-1])
	return reversed_domain + \
		 ('%' + port_path_query if port_path_query is not None else "") + \
		 ('\x01' if schema == "http" else '\x02')


def unreversed_encoded_url(url):
	if not (url.endswith("\x01") or url.endswith("\x02")):
		raise ValueError("Encoded URL must have http or https schema: %r" % (url,))
	rest, schema = url[:-1], url[-1]
	try:
		domain, port_path_query = rest.split("%", 1)
	except ValueError:
		domain = rest
		port_path_query = None
	reversed_domain = '.'.join(domain.split('.')[::-1])
	return ("http%3A%2F%2F" if schema == "\x01" else "https%3A%2F%2F") + \
		 reversed_domain + ('%' + port_path_query if port_path_query is not None else "")


def insert_new_encoded_urls(db, items_root, new_encoded_urls):
	packed_next_item_id = db.get("$next_item_id$", fill_cache=False)
	assert len(packed_next_item_id) == 4, packed_next_item_id
	item_id, = unpack("<I", packed_next_item_id)

	# If URL file has already been written out, abort
	item_fname = get_item_fname(items_root, item_id)
	if os.path.exists(item_fname):
		raise RuntimeError("item_id is %r but %r already exists" % (item_id, item_fname))

	batch = db.newBatch()
	for u in new_encoded_urls:
		db.putTo(batch, reversed_encoded_url(u), packed_next_item_id)
	db.putTo(batch, "$next_item_id$", pack("<I", item_id + 1))
	db.write(batch)

	# The item we write has the normal *not* reversed URLs
	write_item(items_root, item_id, new_encoded_urls)

	new_encoded_urls.clear()


def maybe_insert_new_encoded_urls(db, items_root, new_encoded_urls, num_urls_in_item):
	if len(new_encoded_urls) >= num_urls_in_item:
		insert_new_encoded_urls(db, items_root, new_encoded_urls)


class DBWithCachedIterator(object):
	"""
	As a performance optimization, reuses a db iterator for your
	has() calls (not get()), but throws it away before writing.

	We don't actually need the snapshot functionality of a leveldb
	iterator in this program.  It is actually very dangerous to keep
	a leveldb iterator around because it will prevent leveldb from
	writing to its sorted tree, eventually grinding it to a halt.
	"""
	__slots__ = ['db', 'verify_checksums', 'fill_cache', '_iterator']

	def __init__(self, db, verify_checksums=False, fill_cache=True):
		self.db = db
		self.verify_checksums = verify_checksums
		self.fill_cache = fill_cache
		self._iterator = None


	def _cache_iterator(self):
		self._iterator = self.db.iterator(
			verify_checksums=self.verify_checksums,
			fill_cache=self.fill_cache)


	def _destroy_iterator(self):
		self._iterator.close()
		self._iterator = None


	def has(self, key):
		if not self._iterator:
			self._cache_iterator()
		self._iterator.seek(key)
		return self._iterator.valid() and self._iterator.key() == key


	def get(self, key):
		return self.db.get(
			key,
			verify_checksums=self.verify_checksums,
			fill_cache=self.fill_cache)


	def write(self, batch, sync=False):
		if self._iterator:
			self._destroy_iterator()
		self.db.write(batch, sync)


	def put(self, key, value, sync=False):
		if self._iterator:
			self._destroy_iterator()
		self.db.put(key, value, sync)


	def putTo(self, batch, key, value):
		return self.db.putTo(batch, key, value)


	def newBatch(self):
		return self.db.newBatch()


	def close(self):
		if self._iterator:
			self._destroy_iterator()
		return self.db.close()



def open_db(db_path):
	return leveldb.DB(
		db_path,
		create_if_missing=True,
		write_buffer_size=(64*1024*1024),
		block_cache_size=(128*1024*1024))


def print_progress(n, start, inserted, already):
	end = time.time()
	print "%d\tread at\t%.0f\tURLs/sec, %d\tinserted/queued, %d\talready in db" % (
		n, lines_per_print/float(end - start), inserted, already)


def get_mtime(fname):
	try:
		s = os.stat(fname)
	except OSError:
		return None
	return s.st_mtime


def process_urls(db, items_root, inputf, new_encoded_urls, num_urls_in_item, start_at_input_line):
	stopfile = os.path.join(os.getcwd(), "STOP")
	print "WARNING: To stop, do *not* use ctrl-c; instead, touch %s" % (stopfile,)
	initial_stop_mtime = get_mtime(stopfile)

	# If user hit ctrl-c last time, we may actually have [num_urls_in_item] new_encoded_urls already
	# (We may also have this much if num_urls_in_item is smaller than last time.)
	maybe_insert_new_encoded_urls(db, items_root, new_encoded_urls, num_urls_in_item)

	inserted = 0
	already = 0
	start = time.time()
	n = 0 # Because loop body might never run
	for n, feed_url in enumerate(inputf):
		if n < start_at_input_line:
			continue

		if n != 0 and n % lines_per_print == 0:
			print_progress(n, start, inserted, already)
			inserted = 0
			already = 0
			start = time.time()

			if get_mtime(stopfile) != initial_stop_mtime:
				print "Stopping because %s was touched" % (stopfile,)
				return

		feed_url = feed_url.rstrip()
		if not feed_url:
			continue
		if feed_url.startswith("ftp://"):
			print "Skipping FTP feed %r" % (feed_url,)
			continue
		try:
			feed_url.decode('ascii')
		except UnicodeDecodeError:
			print "Failed to decode as ascii; skipping %r" % (feed_url,)
			continue
		assert feed_url.startswith("http://") or feed_url.startswith("https://"), feed_url
		encoded_url = urllib.quote_plus(feed_url)
		if encoded_url in new_encoded_urls or db.has(reversed_encoded_url(encoded_url)):
			already += 1
			continue
		new_encoded_urls.add(encoded_url)
		inserted += 1

		##print encoded_url, "queued for insertion"

		maybe_insert_new_encoded_urls(db, items_root, new_encoded_urls, num_urls_in_item)

	print_progress(n, start, inserted, already)
	maybe_insert_new_encoded_urls(db, items_root, new_encoded_urls, num_urls_in_item)


def main():
	db_path = sys.argv[1]
	items_root = sys.argv[2]
	# Use ~200 for feeds that are unlikely to 404, ~5000 for those that are
	num_urls_in_item = int(sys.argv[3])
	assert 10 <= num_urls_in_item <= 20000, num_urls_in_item
	try:
		start_at_input_line = int(sys.argv[4])
		assert start_at_input_line >= 0, start_at_input_line
	except IndexError:
		start_at_input_line = 0

	db = open_db(db_path)
	new_encoded_urls_packed = db.get("$new_encoded_urls$")
	if new_encoded_urls_packed: # only want it if it's not None or ""
		new_encoded_urls = set(new_encoded_urls_packed.split("\x00"))
	else:
		new_encoded_urls = set()

	print "Loaded %d new_encoded_urls from db" % (len(new_encoded_urls),)

	try:
		process_urls(db, items_root, sys.stdin, new_encoded_urls, num_urls_in_item, start_at_input_line)
	finally:
		db.put("$new_encoded_urls$", "\x00".join(new_encoded_urls))
		# Not enough URLs for a work item, so store them for next time
		print "Wrote %d new_encoded_urls to db" % (len(new_encoded_urls),)
		db.close()


try: from refbinder.api import bindRecursive
except ImportError: pass
else: bindRecursive(sys.modules[__name__], _postImportVars)

if __name__ == '__main__':
	main()
