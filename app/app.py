from flask import Flask
import psycopg2

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!1</p>"


@app.route("/init")
def init():
    commands = [
        """
        CREATE TABLE test (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """,
    ]

    cfg = {
        "dbname": "postgres",
        "user": "postgres",
        "password": "postgres",
        "host": "postgres",
        "port": 5432,
    }

    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**cfg)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return {"error": str(error)}
    finally:
        if conn is not None:
            conn.close()

    return {"done": True}


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)
