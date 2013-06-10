import argparse
import unittest

from inserter_maker import reversed_encoded_url, unreversed_encoded_url


class InserterMakerTests(unittest.TestCase):
	def test_invalid_reversed(self):
		self.assertRaises(ValueError, lambda: reversed_encoded_url("blah"))
		self.assertRaises(ValueError, lambda: reversed_encoded_url(""))


	def test_invalid_unreversed(self):
		self.assertRaises(ValueError, lambda: unreversed_encoded_url("blah:unknownschema"))
		self.assertRaises(ValueError, lambda: unreversed_encoded_url(""))


	def test_reversed(self):
		# http
		self.assertEqual(
			'com.blah.sub%3A80%2Fpath%3Fquery%3D1%26more%3D2\x01',
			reversed_encoded_url('http%3A%2F%2Fsub.blah.com%3A80%2Fpath%3Fquery%3D1%26more%3D2'))

		# https
		self.assertEqual(
			'com.blah.sub%3A80%2Fpath%3Fquery%3D1%26more%3D2\x02',
			reversed_encoded_url('https%3A%2F%2Fsub.blah.com%3A80%2Fpath%3Fquery%3D1%26more%3D2'))

		# lacking a :port or /path
		self.assertEqual(
			'com.blah.sub\x01',
			reversed_encoded_url('http%3A%2F%2Fsub.blah.com'))


	def test_unreversed(self):
		# http
		self.assertEqual(
			'http%3A%2F%2Fsub.blah.com%3A80%2Fpath%3Fquery%3D1%26more%3D2',
			unreversed_encoded_url('com.blah.sub%3A80%2Fpath%3Fquery%3D1%26more%3D2\x01'))

		# https
		self.assertEqual(
			'https%3A%2F%2Fsub.blah.com%3A80%2Fpath%3Fquery%3D1%26more%3D2',
			unreversed_encoded_url('com.blah.sub%3A80%2Fpath%3Fquery%3D1%26more%3D2\x02'))

		# lacking a :port or /path
		self.assertEqual(
			'http%3A%2F%2Fsub.blah.com',
			unreversed_encoded_url('com.blah.sub\x01'))



def main():
	unittest.main()


if __name__ == "__main__":
	main()
