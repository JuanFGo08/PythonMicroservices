from database.db import get_db_connection


def get_properties_filtered(filters: dict):
	conn = get_db_connection()
	cursor = conn.cursor(dictionary=True)

	query = """
        SELECT
            p.id,
            p.address,
            p.city,
            p.price,
            p.description,
            s.name AS status
        FROM property p
        JOIN status_history h ON h.property_id = p.id
        JOIN status s ON s.id = h.status_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM status_history h2
            WHERE h2.property_id = h.property_id
            AND h2.update_date > h.update_date
        )
        AND s.name IN ('pre_venta', 'en_venta', 'vendido')
    """
	params = []

	if "status" in filters:
		query += " AND name LIKE %s"
		params.append(f"%{filters['status']}%")

	if "year" in filters:
		query += " AND year = %s"
		params.append(filters["year"])

	if "city" in filters:
		query += " AND city = %s"
		params.append(filters["city"])

	cursor.execute(query, tuple(params))
	results = cursor.fetchall()
	cursor.close()
	conn.close()
	return results
