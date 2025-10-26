from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, datetime, os

app = Flask(__name__)
CORS(app)                  # 允许前端跨域
DB = 'health.db'

def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS weight '
                     '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                     'weight REAL NOT NULL, '
                     'record_time TEXT NOT NULL)')

@app.route('/api/weights', methods=['GET'])
def get_weights():
    with sqlite3.connect(DB) as conn:
        rows = conn.execute('SELECT id, weight, record_time FROM weight '
                            'ORDER BY id DESC LIMIT 10').fetchall()
    return jsonify([{'id': r[0], 'weight': r[1], 'date': r[2]} for r in rows])

@app.route('/api/weights', methods=['POST'])
def add_weight():
    data = request.get_json()
    wt = data.get('weight')
    if not wt:
        return jsonify({'error': 'weight required'}), 400
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO weight(weight, record_time) VALUES (?, ?)',
                    (wt, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
    return jsonify({'success': True})

@app.route('/api/weights/<int:pk>', methods=['DELETE'])
def del_weight(pk):
    with sqlite3.connect(DB) as conn:
        conn.execute('DELETE FROM weight WHERE id=?', (pk,))
        conn.commit()
    return jsonify({'success': True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)