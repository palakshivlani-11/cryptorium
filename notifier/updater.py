from datetime import datetime
import os

from apscheduler.schedulers.background import BackgroundScheduler
from notifier import notification

        
#def start():
#        scheduler = BackgroundScheduler()
#        scheduler.add_job(notification.compare, 'interval', minutes=1)
#        scheduler.start()