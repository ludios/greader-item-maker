"""
Imports existing encoded feed URLs with item IDs, without incrementing
$next_item_id$ or writing any URL list files.

If encoded URL already exists in db, will overwrite its assigned item ids.
"""

import os
import sys
import time
from inserter_maker import open_db, get_mtime, encode_item_ids, reversed_encoded_url

_postImportVars = vars().keys()


lines_per_batch_write = 10000

def print_progress(n, start):
	end = time.time()
	print "%d\tread at\t%.0f\tURLs/sec, " % (n, lines_per_batch_write/float(end - start))


def main():
	db_path = sys.argv[1]
	# If item id over this number, don't write that item id to db.
	# If all item ids over this number, don't write item to db at all.
	skip_item_ids_over = int(sys.argv[2], 10)
	# For URLs not written to db at all, append them to this file.
	skip_fname = sys.argv[3]

	stopfile = os.path.join(os.getcwd(), "STOP")
	print "WARNING: To stop, do *not* use ctrl-c; instead, touch %s" % (stopfile,)
	initial_stop_mtime = get_mtime(stopfile)

	with open(skip_fname, "ab") as skips:
		db = open_db(db_path)

		batch = db.newBatch()

		start = time.time()
		for n, line in enumerate(sys.stdin):
			if n != 0 and n % lines_per_batch_write == 0:
				db.write(batch)
				batch = db.newBatch()
				print_progress(n, start)
				start = time.time()

				if get_mtime(stopfile) != initial_stop_mtime:
					print "Stopping because %s was touched" % (stopfile,)
					return

			encoded_feed_url, item_ids_string = line.rsplit("\t", 1)
			# each line in the filtered postgresql dump is "encoded_url\t{num1, num2}" or "{}" if no nums
			item_ids = list(int(n, 10) for n in item_ids_string.strip("}{\r\n").split() if int(n, 10) <= skip_item_ids_over)
			if not item_ids:
				skips.write(encoded_feed_url + "\n")
			else:
				db.putTo(batch, reversed_encoded_url(encoded_feed_url), encode_item_ids(item_ids))

		print_progress(n, start)
		db.write(batch)
		db.close()


try: from refbinder.api import bindRecursive
except ImportError: pass
else: bindRecursive(sys.modules[__name__], _postImportVars)

if __name__ == '__main__':
	main()
