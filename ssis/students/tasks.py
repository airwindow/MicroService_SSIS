from ssis.celery import app

@app.task(queue='students')
def process_student(*args, **kwargs):
    print args
    print kwargs
    return True
