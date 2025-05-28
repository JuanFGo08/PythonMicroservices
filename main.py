import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from mylib.queries import get_properties_filtered


class RequestHandler(BaseHTTPRequestHandler):
	def _set_headers(self, status=200):
		self.send_response(status)
		self.send_header("Content-Type", "application/json")
		self.end_headers()

	def do_GET(self):
		"""
		Handle GET requests to the server.
		The endpoint is designed to filter properties based on query parameters.

		Valid query parameters include:

		- status: Filter properties by their status (e.g., 'en_venta', 'pre_venta').
		- year: Filter properties by the year they were listed.
		- city: Filter properties by city name.

		:return: None

		:raises ValueError: If the year is out of the valid range (1900-2100).
		"""
		parsed_path = urlparse(self.path)
		path_parts = parsed_path.path.strip("/").split("/")

		if path_parts[0] == "properties":
			query_params = parse_qs(parsed_path.query)

			filters = {}
			try:
				if "status" in query_params:
					filters["status"] = query_params["status"][0]

				if "year" in query_params:
					filters["year"] = int(query_params["year"][0])
					if filters["year"] < 1900 or filters["year"] > 2100:
						raise ValueError("Year out of range (1900-2100)")

				if "city" in query_params:
					filters["city"] = query_params["city"][0]

			except ValueError as e:
				self._set_headers(400)
				self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
				return

			properties = get_properties_filtered(filters)
			if not properties:
				self._set_headers(404)
				self.wfile.write(
					json.dumps({"error": "No properties found"}).encode("utf-8")
				)
			else:
				self._set_headers(200)
				self.wfile.write(json.dumps(properties).encode("utf-8"))
		else:
			self._set_headers(403)
			self.wfile.write(json.dumps({"error": "Forbidden"}).encode("utf-8"))


def run_server(port=8000):
	server_address = ("", port)
	httpd = HTTPServer(server_address, RequestHandler)
	logging.info("Server started on port %d", port)
	httpd.serve_forever()


if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	run_server()
