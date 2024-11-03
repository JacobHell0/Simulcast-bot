# from threading import Thread
# from apscheduler.triggers.cron import CronTrigger
from flask import Flask, render_template
from flask_apscheduler import APScheduler
from flask import send_file
from mainProccess import mainProccess
import requests

app = Flask(__name__)

sched = APScheduler()

# Python compiler library: pyinstaller main.py

def send_tracks():
    print("sending")
    mainProccess('s_address')
    # mainProccess('j_address')
    print("sent")

def uptime_ping():
    """ping to indicate uptime"""
    # print("sending ping")
    requests.get("https://hc-ping.com/0ed0d044-b9e5-4341-b772-1e0fa7e28654")
    # print("sent ping")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/manual-send/j')
def manual_send_j():
    mainProccess("j_address")
    return render_template('manual-send-j.html')


@app.route('/manual-send/s')
def manual_send_s():
    mainProccess("s_address")
    return "sent to simulcast, uncomment to work"


@app.route('/RTN_Tracks.pdf')
def return_files_RTN_Tracks():
    try:
        return send_file('RTN_Tracks.pdf', download_name='RTN_Tracks.pdf')
    except Exception as e:
        return str(e)


@app.route('/Track_Sheet.pdf')
def return_files_Track_Sheet():
    try:
        return send_file('Track_sheet.pdf', download_name='Track_sheet.pdf')
    except Exception as e:
        return str(e)


sched.add_job(id='job1', func=send_tracks, trigger='cron', day_of_week='mon-sun', hour=14, minute=0, timezone='UTC')
sched.add_job(id='job2', func=uptime_ping, trigger='cron', minute='*', timezone='UTC')

sched.start()


if __name__ == '__main__':
    # app.run(debug=True, use_reloader=False, host='0.0.0.0', port=8080)
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=8080)
