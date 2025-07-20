from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_cors import CORS
import config
from queries.predefined import register_predefined_routes

app = Flask(__name__)
app.config.from_object(config)
CORS(app)

db = SQLAlchemy(app)

# Models
from models import *

@app.route("/")
def index():
    return "Backend is running!"

@app.route("/db-test")
def db_test():
    try:
        db.session.execute("SELECT 1")
        return "Database connected successfully!"
    except Exception as e:
        return f"DB Error: {str(e)}", 500


# Routes
@app.route('/api/tables/<string:table_name>')
def get_table_data(table_name):
    try:
        sql = text(f'SELECT * FROM "{table_name}"')
        result = db.session.execute(sql)
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in result.fetchall()]
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Register the 8 predefined queries
register_predefined_routes(app, db)

if __name__ == '__main__':
    app.run(debug=True)
