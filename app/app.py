from flask import Flask
from flask import render_template
from challenge import zinobe_challenge
from challenge_parallel import zinobe_challenge_parallel
import sqlite3 as db

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    conn = db.connect('test.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM challenge")
    data = cursor.fetchall()
    cursor.execute("SELECT * FROM metrics")
    metrics = cursor.fetchall()
    metrics_obj = {
        "mean_time": metrics[0][2],
        "max_time": metrics[0][1],
        "min_time": metrics[0][3],
        "total_time": metrics[0][4]
    }
    return {
        "success": True,
        "result": data,
        "metrics": metrics_obj
    }

@app.route('/api/refresh')
def refresh_data():
    challenge = zinobe_challenge()
    challenge.request_info()
    
    return {"success": True}

@app.route('/api/refresh/parallel')
def refresh_data_parallel():
    challenge = zinobe_challenge_parallel()
    challenge.request_info()
    
    return {"success": True}