from flask import Flask, request, jsonify, render_template
import os
import sys
import time

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.core import Database

app = Flask(__name__, template_folder='web/templates')
db = Database("db.json")
db.load()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/tables', methods=['GET'])
def get_tables():
    return jsonify(db.get_tables())

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    sql = data.get('query')
    if not sql:
        return jsonify({"error": "No query provided"}), 400
    
    start_time = time.time()
    try:
        result = db.execute_query(sql)
        duration = time.time() - start_time
        
        # If result is "Error: ...", return as bad request
        if isinstance(result, str) and result.startswith("Error:"):
             return jsonify({"error": result}), 400
             
        # Trigger save on write ops
        if sql.upper().strip().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP')):
            db.save()
            
        # Metadata
        row_count = len(result) if isinstance(result, list) else 1
        meta = {
            "duration_seconds": round(duration, 4),
            "rows_affected": row_count,
            "status": "200 OK"
        }

        return jsonify({"result": result, "meta": meta})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
