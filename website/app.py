from flask import Flask, render_template, redirect
import psycopg2

# Connect to the database
db = 'host=10.17.50.126 dbname=group_18 user=group_18 password=604-287-987'
conn = psycopg2.connect(db)
cur = conn.cursor()

app = Flask(__name__, template_folder='template')


@app.route("/")
def root():
    cur.execute(
    """
        SELECT * FROM playlist_tracks
        ORDER BY random()
        LIMIT 3
    """)
    rows = cur.fetchall()
    print(rows)
    return render_template("base.html", rows=rows)


if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)