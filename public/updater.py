from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from.job import my_scheduled_job
def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(my_scheduled_job,'interval',minutes=1)
    scheduler.start()