import subprocess
import time
import unittest

import requests

BASE_URL = "http://localhost:8000"


class TestServer(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""Start the server before running tests."""
		cls.server = subprocess.Popen(["python", "main.py"])
		time.sleep(1)

	@classmethod
	def tearDownClass(cls):
		"""Terminate the server after tests are done."""
		cls.server.terminate()

	def test_get_properties_return_200(self):
		"""Test that the properties endpoint returns a 200 status code."""
		response = requests.get(f"{BASE_URL}/properties/")
		self.assertEqual(response.status_code, 200)
		self.assertIsInstance(response.json(), list)

	def test_get_properties_with_status_filter_return_200(self):
		"""
		Test that the properties endpoint with status
		filter returns a 200 status code.
		"""
		response = requests.get(f"{BASE_URL}/properties/?status=en_venta")
		self.assertEqual(response.status_code, 200)
		self.assertIsInstance(response.json(), list)

	def test_get_properties_with_year_filter_return_200(self):
		"""
		Test that the properties endpoint with year
		filter returns a 200 status code.
		"""
		response = requests.get(f"{BASE_URL}/properties/?year=2020")
		self.assertEqual(response.status_code, 200)
		self.assertIsInstance(response.json(), list)

	def test_get_properties_with_city_filter_return_200(self):
		"""
		Test that the properties endpoint with city
		filter returns a 200 status code.
		"""
		response = requests.get(f"{BASE_URL}/properties/?city=bogota")
		self.assertEqual(response.status_code, 200)
		self.assertIsInstance(response.json(), list)

	def test_get_properties_with_invalid_year_return_400(self):
		"""
		Test that the properties endpoint with an invalid year
		returns a 400 status code.
		"""
		response = requests.get(f"{BASE_URL}/properties/?year=1800")
		self.assertEqual(response.status_code, 400)
		self.assertIn("error", response.json())

	def test_get_properties_with_invalid_city_return_404(self):
		"""
		Test that the properties endpoint with an invalid city
		returns a 404 status code.
		"""
		response = requests.get(f"{BASE_URL}/properties/?city=invalid_city")
		self.assertEqual(response.status_code, 404)
		self.assertIn("error", response.json())

	def test_get_properties_with_invalid_status_return_404(self):
		"""
		Test that the properties endpoint with an invalid status
		returns a 404 status code.
		"""
		response = requests.get(f"{BASE_URL}/properties/?status=invalid_status")
		self.assertEqual(response.status_code, 404)
		self.assertIn("error", response.json())

	def test_get_properties_with_invalid_endpoint_return_403(self):
		"""
		Test that accessing an invalid endpoint returns a 403 status code.
		"""
		response = requests.get(f"{BASE_URL}/invalid_endpoint")
		self.assertEqual(response.status_code, 403)
		self.assertIn("error", response.json())
