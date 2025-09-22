from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from generate import generate_and_send_report

app = Flask(__name__)

# Basic logging configuration
logging.basicConfig(level=logging.INFO)

# Scheduler setup for periodic tasks (Daily/Weekly)
scheduler = BackgroundScheduler()

def schedule_daily_report():
    scheduler.add_job(
        generate_and_send_report, 
        trigger=IntervalTrigger(hours=24, start_date="2025-09-22 08:00:00"), 
        id="daily_report", 
        replace_existing=True
    )
    scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_report', methods=['POST'])
def send_report():
    # Trigger report generation and email sending on demand (for testing)
    try:
        generate_and_send_report()
        return jsonify({"message": "Report sent successfully!"}), 200
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    schedule_daily_report()
    app.run(debug=True, use_reloader=False)  # use_reloader=False to avoid APScheduler duplication
