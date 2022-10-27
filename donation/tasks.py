from Lifo_and_Fifo_Django.celery import app


@app.task
def add(x, y):
    return x + y
