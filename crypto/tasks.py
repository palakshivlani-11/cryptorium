from celery.task.schedules import crontab
from celery.decorators import periodic_task
from .models import *
import requests
import json
from django.shortcuts import render
from django.template.loader import render_to_string 
from django.core.mail import EmailMessage




def send_buy_notifications(name,email,coin,coinprice,fetchprice):
    html_version = 'buynotification.html'
    context = {
            'title':"Knock! Knock! Great Opportunity",
            'name' : name
             
        }
    html_message = render_to_string(html_version,context)
    subject = "Knock Knock! Great Opportunity is waiting!"
    to_email = email
    text = "Hey! " + name + ", Your coin" + coin + " has reached price "+" ₹" + str(fetchprice) +  " .Its best time to buy your favourite coin."
    message = EmailMessage(subject, text,'palakshivlani2001@gmail.com', [to_email])
    #message.content_subtype = 'html' # this is required because there is no plain text email version
    message.send()


def send_sell_notifications(name,email,coin,coinprice,fetchprice):
    html_version = 'sellnotification.html'
    context = {
            'title':"Knock! Knock! Great Opportunity",
            'name' : name
             
        }
    html_message = render_to_string(html_version,context)
    subject = "Knock Knock! Great Opportunity is waiting!"
    to_email = email
    text = "Hey! " + name + ", Your coin" + coin + " has reached price "+" ₹" + str(fetchprice) +  " .Its best time to sell your favourite coin."
    message = EmailMessage(subject, text,'palakshivlani2001@gmail.com', [to_email])
    #message.content_subtype = 'html' # this is required because there is no plain text email version
    message.send()

def send_notifications(name,email):
    html_version = 'normalnotification.html'
    context = {
            'title':"Knock! Knock! Keep Updating Yourself",
            'name' : name
             
        }
    html_message = render_to_string(html_version,context)
    subject = "Knock Knock! Keep Updating Yourself"
    to_email = email
    text = " Hey ! " + name + " Keep Updating Yourself "
    message = EmailMessage(subject, text,'palakshivlani2001@gmail.com', [to_email])
    #message.content_subtype = 'html' # this is required because there is no plain text email version
    message.send()


#@periodic_task(run_every=crontab(minute='*/1', day_of_week="*"))
def cryptoprices(quote):
     price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=" + quote + "&tsyms=INR")
     price = json.loads(price_request.content)
     #print(price['RAW'][quote]['INR']['PRICE'])
     return price['RAW'][quote]['INR']['PRICE']


@periodic_task(run_every=crontab(minute='*/240', day_of_week="*"))
def compare():
    obj = Notification.objects.all()
    for i in obj:
        user = i.us.username
        mail = i.us.email
        c = i.coin
        p = i.coinprice
        fetch = cryptoprices(c)
        if fetch < p:
            send_buy_notifications(user,mail,c,p,fetch)
        elif fetch > p:
            send_sell_notifications(user,mail,c,p,fetch)
        else:
            send_notifications(user,mail)
    print(obj)



