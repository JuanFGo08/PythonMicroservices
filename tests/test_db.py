import pytest
import unittest
from mysql.connector import DatabaseError

from database.config import DB_CONFIG
from database.db import get_db_connection


class TestDatabase(unittest.TestCase):
	"""Test suite for database connection and error handling."""

	@classmethod
	def setUpClass(cls):
		"""Set up the database connection before running tests."""
		cls.conn = get_db_connection()

	@classmethod
	def tearDownClass(cls):
		"""Close the database connection after tests are done."""
		if cls.conn.is_connected():
			cls.conn.close()

	def test_get_db_connection(self):
		"""Test the database connection."""
		try:
			conn = get_db_connection()
			assert conn.is_connected(), "Database connection should be established"
		except Exception as e:
			raise AssertionError(f"Database connection failed: {e}") from e
		finally:
			if conn.is_connected():
				conn.close()


	def test_get_db_connection_error(self):
		"""Test the database connection error handling."""
		original_config = DB_CONFIG.copy()

		# Temporarily modify the DB_CONFIG to force a connection error
		DB_CONFIG["host"] = "invalid_host"

		try:
			with pytest.raises(DatabaseError):
				get_db_connection()
		finally:
			# Restore the original configuration
			DB_CONFIG.update(original_config)
