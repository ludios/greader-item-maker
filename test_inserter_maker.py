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
			'com.blah.sub%3A80%2Fpath%3Fquery%3D1%26more%3D2:http',
			reversed_encoded_url('http%3A%2F%2Fsub.blah.com%3A80%2Fpath%3Fquery%3D1%26more%3D2'))

		# https
		self.assertEqual(
			'com.blah.sub%3A80%2Fpath%3Fquery%3D1%26more%3D2:https',
			reversed_encoded_url('https%3A%2F%2Fsub.blah.com%3A80%2Fpath%3Fquery%3D1%26more%3D2'))


	def test_unreversed(self):
		# http
		self.assertEqual(
			'http%3A%2F%2Fsub.blah.com%3A80%2Fpath%3Fquery%3D1%26more%3D2',
			unreversed_encoded_url('com.blah.sub%3A80%2Fpath%3Fquery%3D1%26more%3D2:http'))

		# https
		self.assertEqual(
			'https%3A%2F%2Fsub.blah.com%3A80%2Fpath%3Fquery%3D1%26more%3D2',
			unreversed_encoded_url('com.blah.sub%3A80%2Fpath%3Fquery%3D1%26more%3D2:https'))



def main():
	unittest.main()


if __name__ == "__main__":
	main()
