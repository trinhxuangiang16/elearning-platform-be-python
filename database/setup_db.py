import os
import ssl
import pymysql
from dotenv import load_dotenv


def get_db_connection(include_db=False):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    load_dotenv(env_path)

    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "3306"))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "elearning_python_db")
    use_ssl = os.getenv("DB_SSL", "False").lower() == "true"

    conn_kwargs = {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "charset": "utf8mb4",
        "autocommit": True,
        "cursorclass": pymysql.cursors.DictCursor,
    }

    if include_db:
        conn_kwargs["database"] = db_name

    if use_ssl:
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        conn_kwargs["ssl"] = ssl_ctx

    return pymysql.connect(**conn_kwargs)


def execute_sql_script(cursor, sql_text):
    statements = []
    current_lines = []

    for line in sql_text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("--") or stripped.startswith("/*"):
            continue
        current_lines.append(line)
        if stripped.endswith(";"):
            statement = "\n".join(current_lines).strip()
            statements.append(statement)
            current_lines = []

    if current_lines:
        statements.append("\n".join(current_lines).strip())

    for stmt in statements:
        if stmt:
            cursor.execute(stmt)


def setup_database():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_path = os.path.join(base_dir, ".env")
    load_dotenv(env_path)
    db_name = os.getenv("DB_NAME", "elearning_python_db")

    server_conn = get_db_connection(include_db=False)
    with server_conn.cursor() as cursor:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        )
    server_conn.close()

    db_conn = get_db_connection(include_db=True)
    with db_conn.cursor() as cursor:
        init_sql_path = os.path.join(base_dir, "database", "init_elearning_python_db.sql")
        if os.path.exists(init_sql_path):
            with open(init_sql_path, "r", encoding="utf-8") as f:
                init_sql = f.read()
            execute_sql_script(cursor, init_sql)

        cursor.execute("SHOW TABLES;")
        tables = [list(r.values())[0] for r in cursor.fetchall()]
        print(f"Database initialized successfully ({len(tables)} tables).")
    db_conn.close()


if __name__ == "__main__":
    setup_database()
