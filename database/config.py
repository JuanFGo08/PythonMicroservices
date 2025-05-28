from decouple import config

DB_CONFIG = {
	"host": config("DB_HOST", default="localhost"),
	"port": config("DB_PORT", default="3306"),
	"user": config("DB_USER", default="root"),
	"password": config("DB_PASSWORD", default="password"),
	"database": config("DB_NAME", default="mydatabase"),
}
