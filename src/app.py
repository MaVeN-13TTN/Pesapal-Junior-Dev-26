from flask import Flask, request, jsonify, render_template
from src.db.core import Database
import os

app = Flask(__name__, template_folder='templates')
db = Database("db.json")
db.load()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    sql = data.get('query')
    if not sql:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        result = db.execute_query(sql)
        # If result is "Error: ...", return as bad request or just normal with error field?
        # Our execute_query returns string "Error: ..." on exception catch.
        if isinstance(result, str) and result.startswith("Error:"):
             return jsonify({"error": result}), 400
             
        # Trigger save on write ops?
        if sql.upper().strip().startswith(('INSERT', 'UPDATE', 'DELETE', 'CREATE')):
            db.save()
            
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000)
