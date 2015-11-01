from ssis.celery import app

@app.task(queue='students', routing_key='students.request')
def process_student(self, request):
    print 'process_student'
    print request
    return True
