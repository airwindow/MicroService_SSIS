from ssis.celery import app

@app.task(bind=True)
def route_request(self, *args, **kwargs):
    print self
    print args
    print kwargs
    request = args[0]
    print request
    response = self.apply_async(args=[request], queue='students', routing_key='students.list')
    print response
    return response
