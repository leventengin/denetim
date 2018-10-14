from __future__ import absolute_import, unicode_literals
#from denetim.celery import app

app = Celery('denetim',
             broker='amqp://',
             backend='amqp://',
             include=['tasks'])

app.config_from_object('celeryconfig')

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)
