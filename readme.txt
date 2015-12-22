-----------------------------------------------------
README
------------------------------------------------------

What it is?
----------------------------------------------------
This implementation is our final project for course Micro-Service Apps & APIs at Columbia University. 
The great class was taught by Professor Donald F Ferguso. 
In this project, we simulate the real-life IT situation of an organization and explore the benefits of Micro-Service and Multi-tenancy. 


Project Structure
-------------------------------------------------------
Our project was consisted of four components
1. K12 Service (hsinfo directory). 
This component was backed by DynamoDB, which records the basic information of students.
It uses Django REST Framework to provide CRUD RESTful API to manage K12 information. 


2. Student Finance Service (student_saas directory)
This component was backed by sqlite database, which records the basic financial information of students.
Besides providing CRUD RESTful API to manage student's financial information, it also supports multi-tenancy. 
Thus, it also provides RESTful API for managing tenant and their respective schema. 


3. API Gateway worker (APIGateWay directory)
This component is used for simulating the architecture using SQS and Gateway.
API Gateway worker owns a queue and periodically reads message from the queue, then proxy the request for the client who sent the message. 

4. Client (Client1 directory)
The one who send the message to API Gateway. 
It request services through API Gateway rather than call them directly. 
All test cases were defined at here. 


Installation
-------------------------------------------------------
1. start K12 Service (current dierctory: hsinfo)
1.1 start DynamoDB local server 
students/DynamoDB/rundb.sh

1.2 run K12 Service at port 8111 
python manage.py runserver 8111


2. start student finance service (current directory: student_saas)
2.1 empty sqlite3 database
rm db.sqlite3
python manage.py migrate
2.2 run student finance service at port 8000
python manage.py runserver 8000


3. start APIGateway worker (current directory: APIGateWay)
python gateway_worker.py

4. start Client worker (current directory: Client1)
(You can customize all your test cases at here)
python clientWorker.py 


Test
-------------------------------------------------------
We have listed functional test cases of this project at  "test/test.txt".
You can directly test them through RESTful API.



Note 
-------------------------------------------------------
Since we use Amazon's SQS service, please have your AWS credential configured properly. 
You also need to create two queue for using this system.
1. APIGateWayQueue
2. ClientOneQueue



Thanks
-------------------------------------------------------
Through this great class, we have learned a lot about modern architecture of Enterprise. 
The introduction of SQS and Multi-tenancy is really interesting and useful.

Great thanks to the dedicated works of Professor and TAs!