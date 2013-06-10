import os
import sys
import urllib
import gzip
import time
from struct import pack, unpack

# https://code.google.com/p/leveldb-py/
import leveldb

_postImportVars = vars().keys()


num_urls_in_item = 200

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
		f.write("\n".join(encoded_urls) + "\n")
	finally:
		f.close()
	assert not os.path.exists(fname), fname
	os.rename(fname + ".tmp", fname)


def encode_item_ids(ids):
	return "".join(pack("<I", n) for n in ids)


def decode_item_ids(ids):
	return unpack("<I", ids)


def reversed_encoded_url(url):
	# TODO XXX ENCODE THESE URLs into reverse.domain.format
	return url


def insert_new_encoded_urls(db, items_root, new_encoded_urls):
	assert len(new_encoded_urls) == num_urls_in_item, new_encoded_urls
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

	del new_encoded_urls[:]


def maybe_insert_new_encoded_urls(db, items_root, new_encoded_urls):
	assert len(new_encoded_urls) <= num_urls_in_item, new_encoded_urls
	if len(new_encoded_urls) == num_urls_in_item:
		insert_new_encoded_urls(db, items_root, new_encoded_urls)


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


def process_urls(db, items_root, inputf, new_encoded_urls):
	stopfile = os.path.join(os.getcwd(), "STOP")
	print "WARNING: To stop, do *not* use ctrl-c; instead, touch %s" % (stopfile,)
	initial_stop_mtime = get_mtime(stopfile)

	# If user hit ctrl-c last time, we may actually have 200 new_encoded_urls already
	maybe_insert_new_encoded_urls(db, items_root, new_encoded_urls)

	inserted = 0
	already = 0
	start = time.time()
	for n, feed_url in enumerate(inputf):
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
		try:
			feed_url.decode('ascii')
		except UnicodeDecodeError:
			print "Failed to decode as ascii; skipping %r" % (feed_url,)
			continue
		assert feed_url.startswith("http://") or feed_url.startswith("https://"), feed_url
		encoded_url = urllib.quote_plus(feed_url)
		if db.has(reversed_encoded_url(encoded_url)):
			already += 1
			continue
		new_encoded_urls.append(encoded_url)
		inserted += 1

		##print encoded_url, "queued for insertion"

		maybe_insert_new_encoded_urls(db, items_root, new_encoded_urls)

	print_progress(n, start, inserted, already)
	maybe_insert_new_encoded_urls(db, items_root, new_encoded_urls)


def main():
	db_path = sys.argv[1]
	items_root = sys.argv[2]

	db = open_db(db_path)
	new_encoded_urls = db.get("$new_encoded_urls$").split("\x00")
	if new_encoded_urls is None:
		new_encoded_urls = []

	print "Loaded %d new_encoded_urls from db" % (len(new_encoded_urls),)

	try:
		process_urls(db, items_root, sys.stdin, new_encoded_urls)
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
