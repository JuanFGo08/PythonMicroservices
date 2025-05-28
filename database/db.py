import mysql.connector
from mysql.connector import DatabaseError

from .config import DB_CONFIG


def get_db_connection():
	"""Establish a connection to the MySQL database."""
	try:
		return mysql.connector.connect(**DB_CONFIG)
	except mysql.connector.Error as err:
		msg = f"Failed to connect to the database: {err}"
		raise DatabaseError(msg) from err
